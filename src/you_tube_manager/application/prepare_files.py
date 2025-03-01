# ======================================================================
# MODULE DETAILS
# This section provides metadata about the module, including its
# creation date, author, copyright information, and a brief description
# of the module's purpose and functionality.
# ======================================================================

#   __|    \    _ \  |      _ \   __| __ __| __ __|
#  (      _ \     /  |     (   | (_ |    |      |
# \___| _/  _\ _|_\ ____| \___/ \___|   _|     _|

# src/you_tube_manager/application/prepare_files.py
# Created 3/1/25 - 6:58 PM UK Time (London) by carlogtt
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
import os
import string

# END IMPORTS
# ======================================================================


# List of public names in the module
# __all__ = []

# Setting up logger for current module
# module_logger =

# Type aliases
#


ALLOWED_PATTERN = string.ascii_letters + string.digits + '&+,-;=^ '
NOT_ALLOWED_CHAR = '^+;'

ROOT_DIR = '/Users/carlogtt/Downloads/Linux_Deep_Dive/extract/Linux_Deep_Dive'
MOVE_DIR = '/Users/carlogtt/Downloads/Linux_Deep_Dive/extract/Linux_Deep_Dive_Moved'


def rename_files() -> None:
    """ """

    for root, dirs, files in os.walk(ROOT_DIR):
        for video_dir in dirs:
            for root1, dirs1, files1 in os.walk(f"{ROOT_DIR}/{video_dir}"):
                for video_file in files1:

                    if video_file[-4:] != '.mp4':
                        print(f"[SKIPPING FILE] - {ROOT_DIR}/{video_dir}/{video_file}")
                        continue

                    # file is a .mp4 so process it
                    folder_id = video_dir[:2]
                    video_id = video_file[:3]
                    video_tile = video_file[4:-4]

                    youtube_name = f"{folder_id}-{video_id} - {video_tile}"

                    for char in youtube_name:
                        if char in NOT_ALLOWED_CHAR:
                            youtube_name_bak = youtube_name
                            youtube_name = youtube_name.replace(char, '')
                            print(f"[REPLACING CHAR] - {youtube_name_bak} with {youtube_name}")

                    src = f"{ROOT_DIR}/{video_dir}/{video_file}"
                    dst = f"{MOVE_DIR}/{youtube_name}"

                    print(src)
                    print(dst)
                    # os.rename(src, dst)
