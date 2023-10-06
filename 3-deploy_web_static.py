#!/usr/bin/python3
# File: 3-deploy_web_static.py
# Author: Oluwatobiloba Light
"""Fabric script that creates and distributes an archive to your web servers"""
from fabric.api import run, put, env, local
from datetime import datetime
import os

env.hosts = ['204.236.240.195', '52.91.123.82	']
env.user = 'ubuntu'


def do_pack():
    """
    Archive the contents of the web_static folder into a .tgz file.
    """
    dt = datetime.utcnow()
    filename = "{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    try:
        # Check if 'versions' directory exists; create it if not
        if not os.path.isdir('versions'):
            local('mkdir -p versions')

        # Create the archive
        file = local(
            'tar -czvf versions/web_static_{} web_static'.format(filename))

        # Check if the archive creation failed
        if file.failed:
            return None
        return file

    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distribute an archive to web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        archive_name = os.path.basename(archive_path.split("/")[-1].
                                        split('.')[0])
        remote_path = "/tmp/{}".format(archive_name)
        put(archive_name, remote_path)

        # Create a new folder for the archive
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(
            archive_name))

        # Uncompress the archive to the new version directory
        run('sudo tar -xzf {} -C /data/web_static/releases/{}/'.
            format(remote_path, archive_name))

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


def deploy():
    """Creates and distributes an archive to your web servers"""
    file = do_pack()
    if file is None:
        return False
    file = do_deploy(file)
    return file
