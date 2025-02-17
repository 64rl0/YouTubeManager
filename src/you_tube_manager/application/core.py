# ======================================================================
# MODULE DETAILS
# This section provides metadata about the module, including its
# creation date, author, copyright information, and a brief description
# of the module's purpose and functionality.
# ======================================================================

#   __|    \    _ \  |      _ \   __| __ __| __ __|
#  (      _ \     /  |     (   | (_ |    |      |
# \___| _/  _\ _|_\ ____| \___/ \___|   _|     _|

# src/you_tube_manager/application/core.py
# Created 2/17/25 - 7:57 AM UK Time (London) by carlogtt
# Copyright (c) Amazon.com Inc. All Rights Reserved.
# AMAZON.COM CONFIDENTIAL

"""
This module ...
"""

# ======================================================================
# EXCEPTIONS
# This section documents any exceptions made code or quality rules.
# These exceptions may be necessary due to specific coding requirements
# or to bypass false positives.
# ======================================================================
#

# ======================================================================
# IMPORTS
# Importing required libraries and modules for the application.
# ======================================================================

# Standard Library Imports
import http.client
import os
import time

# Third Party Library Imports
import apiclient  # type: ignore
import httplib2
import oauth2client.client  # type: ignore
import oauth2client.file  # type: ignore
import oauth2client.tools  # type: ignore

# Local Folder (Relative) Imports
from .. import config

# END IMPORTS
# ======================================================================


# List of public names in the module
__all__ = ['YouTubeManager']

# Setting up logger for current module
# module_logger =

# Type aliases
#


# Explicitly tell the underlying HTTP transport library not to retry,
# since we are handling retry logic ourselves.
httplib2.RETRIES = 1


class YouTubeManager:

    # The CLIENT_SECRETS_FILE variable specifies the name of a file that
    # contains the OAuth 2.0 information for this application, including
    # its client_id and client_secret. You can acquire an OAuth 2.0
    # client ID and client secret from the Google API Console at
    # https://console.cloud.google.com/.
    # Please ensure that you have enabled the YouTube Data API for your
    # project. For more information about using OAuth2 to access the
    # YouTube Data API, see:
    # https://developers.google.com/youtube/v3/guides/authentication
    # For more information about the client_secrets.json file format,
    # see:
    # https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    CLIENT_SECRETS_FILE = os.path.join(config.PROJECT_ROOT_DIR, 'oauth2', 'client_secrets.json')
    OAUTH2_FILE = os.path.join(config.PROJECT_ROOT_DIR, 'oauth2', 'oauth2.json')

    # This OAuth 2.0 access scope allows an application to upload files
    # to the authenticated user's YouTube channel, but doesn't allow
    # other types of access.
    YOUTUBE_UPLOAD_SCOPE = (
        "https://www.googleapis.com/auth/youtube.upload"
        " https://www.googleapis.com/auth/youtube.force-ssl"
    )
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    # This variable defines a message to display if the
    # CLIENT_SECRETS_FILE is missing.
    MISSING_CLIENT_SECRETS_MESSAGE = f"""
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the client_secrets.json file
    found at:

       {os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))}

    with information from the API Console
    https://console.cloud.google.com/

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """

    # Maximum number of times to retry before giving up.
    MAX_RETRIES = 10

    # Always retry when an apiclient.errors.HttpError with one of these
    # status codes is raised.
    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

    # Always retry when these exceptions are raised.
    RETRIABLE_EXCEPTIONS = (
        IOError,
        httplib2.HttpLib2Error,
        http.client.NotConnected,
        http.client.IncompleteRead,
        http.client.ImproperConnectionState,
        http.client.CannotSendRequest,
        http.client.CannotSendHeader,
        http.client.ResponseNotReady,
        http.client.BadStatusLine,
    )

    def __init__(self):
        self.youtube = None

    def authenticate(self, args):
        flow = oauth2client.client.flow_from_clientsecrets(
            self.CLIENT_SECRETS_FILE,
            scope=self.YOUTUBE_UPLOAD_SCOPE,
            message=self.MISSING_CLIENT_SECRETS_MESSAGE,
        )

        storage = oauth2client.file.Storage(self.OAUTH2_FILE)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = oauth2client.tools.run_flow(flow, storage, args)

        self.youtube = apiclient.discovery.build(
            serviceName=self.YOUTUBE_API_SERVICE_NAME,
            version=self.YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()),
        )

    def upload_video(
        self, file: str, title: str, description: str, category: str, privacy_status: str, tags: str
    ):
        """

        :param file:
        :param title:
        :param description:
        :param category:
        :param privacy_status:
        :param tags:
        :return:
        """

        if not self.youtube:
            raise ConnectionError("YouTube service not authenticated")

        if not os.path.exists(file):
            raise FileNotFoundError(f"File '{file}' not found")

        if tags:
            tags_list = tags.split(",")
        else:
            tags_list = None

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags_list,
                'categoryId': category,
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False,
            },
        }

        # Call the API's videos.insert method to create and upload the
        # video.
        insert_request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk
            # of data, in bytes, that will be uploaded at a time. Set a
            # higher value for reliable connections as fewer chunks
            # lead to faster uploads. Set a lower value for better
            # recovery on less reliable connections.
            #
            # Setting "chunksize" equal to -1 in the code below means
            # that the entire file will be uploaded in a single HTTP
            # request. (If the upload fails, it will still be retried
            # where it lefr off.) This is usually a best practice, but
            # if you're using Python older than 2.6 or if you're running
            # on App Engine, you should set the chunksize to something
            # like 1024 * 1024 (1 megabyte).
            media_body=apiclient.http.MediaFileUpload(file, chunksize=-1, resumable=True),
        )

        response = self._resumable_upload(insert_request)

        return response

    def add_video_to_playlist(self, video_id, playlist_id):
        """

        :param video_id:
        :param playlist_id:
        """

        if not self.youtube:
            raise ConnectionError("YouTube service not authenticated")

        add_request = self.youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id,
                    },
                }
            },
        )

        response = add_request.execute()  # noqa
        print(f"  Video was successfully added to playlist '{playlist_id}'")

    def _resumable_upload(self, insert_request):
        """
        This method implements an exponential backoff strategy to
        resume a failed upload.

        :param insert_request:
        :return:
        """

        response = None
        error = None
        retry = 0

        while response is None:
            try:
                print("  Uploading video...")
                _, response = insert_request.next_chunk()
                if response is not None:
                    if response.get('id'):
                        print(f"  Video id '{response['id']}' was successfully uploaded.")
                        return response
                    else:
                        print(f"  The upload failed with an unexpected response: {response}")

            except apiclient.errors.HttpError as ex:
                if ex.resp.status in self.RETRIABLE_STATUS_CODES:
                    error = f"  A retriable HTTP error {ex.resp.status} occurred:\n{ex.content}"
                    print(error)
                else:
                    raise

            except self.RETRIABLE_EXCEPTIONS as ex:
                error = f"  A retriable error occurred: {ex}"
                print(error)

            if error is not None:
                retry += 1
                if retry > self.MAX_RETRIES:
                    print("  No longer attempting to retry.")
                    break
                sleep_seconds = 2**retry
                print(f"  Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)
