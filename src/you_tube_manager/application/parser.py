# ======================================================================
# MODULE DETAILS
# This section provides metadata about the module, including its
# creation date, author, copyright information, and a brief description
# of the module's purpose and functionality.
# ======================================================================

#   __|    \    _ \  |      _ \   __| __ __| __ __|
#  (      _ \     /  |     (   | (_ |    |      |
# \___| _/  _\ _|_\ ____| \___/ \___|   _|     _|

# src/you_tube_manager/application/parser.py
# Created 2/17/25 - 8:25 AM UK Time (London) by carlogtt
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

# Third Party Library Imports
import oauth2client.tools  # type: ignore

# END IMPORTS
# ======================================================================


# List of public names in the module
__all__ = ['parse_args']

# Setting up logger for current module
# module_logger =

# Type aliases
#


def parse_args() -> argparse.Namespace:
    oauth2client.tools.argparser.add_argument(
        "--file",
        required=True,
        help="Video file to upload",
    )
    oauth2client.tools.argparser.add_argument(
        "--title",
        required=False,
        help="Video title",
        default="Title",
    )
    oauth2client.tools.argparser.add_argument(
        "--description",
        required=False,
        help="Video description",
        default="Description",
    )
    oauth2client.tools.argparser.add_argument(
        "--category",
        required=True,
        help="Numeric video category. See https://gist.github.com/dgp/1b24bf2961521bd75d6c",
    )
    oauth2client.tools.argparser.add_argument(
        "--tags",
        required=False,
        help="Video tags, comma separated",
        default=None,
    )
    oauth2client.tools.argparser.add_argument(
        "--privacy_status",
        required=False,
        help="Video privacy status.",
        choices=("public", "private", "unlisted"),
        default="private",
    )
    oauth2client.tools.argparser.add_argument(
        "--playlist_id",
        required=False,
        help="Playlist to add the video to",
        default="",
    )

    args = oauth2client.tools.argparser.parse_args()

    return args
