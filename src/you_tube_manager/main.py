# ======================================================================
# MODULE DETAILS
# This section provides metadata about the module, including its
# creation date, author, copyright information, and a brief description
# of the module's purpose and functionality.
# ======================================================================

#   __|    \    _ \  |      _ \   __| __ __| __ __|
#  (      _ \     /  |     (   | (_ |    |      |
# \___| _/  _\ _|_\ ____| \___/ \___|   _|     _|

# src/you_tube_manager/main.py
# Created 1/25/24 - 10:07 PM UK Time (London) by carlogtt
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
import argparse
import json

# Local Folder (Relative) Imports
from . import application, config

# END IMPORTS
# ======================================================================


# List of public names in the module
__all__ = ['main']

# Setting up logger for current module
# module_logger =

# Type aliases
#


def upload_videos(args: argparse.Namespace):
    try:
        youtube = application.YouTubeManager()
        youtube.authenticate(args)
        response = youtube.upload_video(
            file=args.file,
            title=args.title,
            description=args.description,
            category=args.category,
            tags=args.tags,
            privacy_status=args.privacy_status,
        )

        return response

    except Exception as ex:
        print(repr(ex))


def add_video_to_playlist(args: argparse.Namespace, video_id: str, playlist_id: str):
    try:
        youtube = application.YouTubeManager()
        youtube.authenticate(args)
        youtube.add_video_to_playlist(
            video_id=video_id,
            playlist_id=playlist_id,
        )

    except Exception as ex:
        print(repr(ex))


def get_all_channel_videos(args: argparse.Namespace):
    try:
        youtube = application.YouTubeManager()
        youtube.authenticate(args)

        response = youtube.get_channel_videos('UCokerZd5tsOb5W8t48O6kYQ')

        with open(f'{config.STATIC_FOLDER}/channel-videos.json', 'w') as out_file:
            out_file.write(json.dumps(response, indent=4))

    except Exception as ex:
        print(repr(ex))


def get_all_playlist_videos(args: argparse.Namespace):
    try:
        youtube = application.YouTubeManager()
        youtube.authenticate(args)

        response = youtube.get_playlist_videos('PLMYoPW_jBFB73NMBkiOgp9peJ9O962US_')

        with open(f'{config.STATIC_FOLDER}/python-playlist-videos.json', 'w') as out_file:
            out_file.write(json.dumps(response, indent=4))

    except Exception as ex:
        print(repr(ex))


def get_all_videos_list(file: str):
    with open(f'{config.STATIC_FOLDER}/{file}', 'r') as out_file:
        data = json.load(out_file)

    videos = [
        (video['snippet']['resourceId']['videoId'], video['snippet']['title'])
        for video in data['items']
    ]

    return videos


def main() -> None:
    args = application.parse_args()

    response = upload_videos(args)
    add_video_to_playlist(args, response['id'], args.playlist_id)
