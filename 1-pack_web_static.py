#!/usr/bin/python3
# File: 1-pack_web_static.py
# Author: Oluwatobiloba Light
"""Generates a .tgz archive from the contents of the web_static folder"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Archive the contents of the web_static folder into a .tgz archive.
    """
    dt = datetime.utcnow()
    filename = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    try:
        # Check if 'versions' directory exists; create it if not
        if not os.path.isdir('versions'):
            local('mkdir -p versions')

        # Create the archive
        archive = local(
            'tar -czvf {} web_static'.format(filename))

        # Check if the archive creation failed
        if archive.failed is True:
            return None
        return filename

    except Exception as e:
        return None

    # if os.path.isdir('versions') is False:
    #     versions = local('mkdir -p versions')
    #     if versions.failed is True:
    #         return None
    # archive = local('tar -czvf versions/web_static_{}'.format(filename))
    # if archive.failed is True:
    #     return None
    # return archive
