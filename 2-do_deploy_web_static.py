#!/usr/bin/python3
# File: 2-do_deploy_web_static.py
# Author: Oluwatobiloba Light
"""Fabric script to distribute an archive to your web servers"""
from fabric.api import task, run, put, run, env
import os


env.hosts = ['204.236.240.195', '34.239.253.9']


@task
def do_deploy(archive_path):
    """
    Distribute an archive to web servers.
    """
    try:
        if not os.path.exists(archive_path):
            return False

        # Upload the archive to /tmp/ directory on the web server
        filename = os.path.basename(archive_path.split("/")[-1])
        archive_name = os.path.basename(filename.split('.')[0])
        dir_path = "/data/web_static/releases/"

        # Upload file to remote server
        put(archive_path, "/tmp/")

        run("sudo rm -rf {}{}/".format(dir_path, archive_name))

        # Create a new folder for the archive
        run('sudo mkdir -p {}{}/'.format(dir_path, archive_name))

        # Uncompress the archive to the new version directory
        run('sudo tar -xzf /tmp/{} -C {}{}/'.
            format(filename, dir_path, archive_name))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(filename))

        # Move contents into the host web_static
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.
            format(dir_path, archive_name))

        # Delete web_static compressed directory & files
        run('sudo rm -rf {}{}/web_static'.format(dir_path, archive_name))

        # Delete the symbolic link from the web server
        run('sudo rm -rf /data/web_static/current')
#
        # # Create a new symbolic link
        run('sudo ln -sf {}{}/ \
            /data/web_static/current'.format(dir_path, archive_name))
        # print("New version deployed!")
        return True
    except Exception:
        return False
