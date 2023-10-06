#!/usr/bin/python3
# File: 2-do_deploy_web_static.py
# Author: Oluwatobiloba Light
"""Fabric script to distribute an archive to your web servers"""
from fabric.api import run, put
import os


env.hosts = ['204.236.240.195', '52.91.123.82	']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distribute an archive to web servers.
    """
    if os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        archive_name = os.path.basename(archive_path.split("/")[-1].
                                        split('.')[0])
        remote_path = "/tmp/{}".format(archive_name)
        put(archive_name, remote_path)

        # Create a new folder for the archive
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(
            archive_name.split('.')[0]))

        # Uncompress the archive to the new version directory
        run('sudo tar -xzf {} -C /data/web_static/releases/{}/'.
            format(remote_path, archive_name.split('.')[0]))

        # Delete the archive from the web server
        run('sudo rm {}'.format(remote_path))

        # Move contents into the host web_static
        run('sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(archive_name,
                                                  archive_name))

        # Delete web_static compressed directory & files
        run('rm -rf /data/web_static/releases/{}/web_static')

        # Delete the symbolic link from the web server
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('sudo ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(archive_name))
    except:
        return False

    return True
