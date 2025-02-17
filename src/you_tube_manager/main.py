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

# Local Folder (Relative) Imports
from . import application

# END IMPORTS
# ======================================================================


# List of public names in the module
__all__ = ['main']

# Setting up logger for current module
# module_logger =

# Type aliases
#


def main() -> None:

    args = application.parse_args()

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
        youtube.add_video_to_playlist(
            video_id=response['id'],
            playlist_id=args.playlist_id,
        )

    except Exception as ex:
        print(repr(ex))
