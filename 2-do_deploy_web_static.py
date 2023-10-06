#!/usr/bin/python3
# File: 2-do_deploy_web_static.py
# Author: Oluwatobiloba Light
"""Fabric script to distribute an archive to your web servers"""
from fabric.api import *
import os


env.hosts = ['204.236.240.195', '34.239.253.9']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distribute an archive to web servers.
    """
#     try:
#         # filename = os.path.basename(archive_path.split("/")[-1])
#         # archive_name = os.path.basename(filename.split('.')[0])
#         if not os.path.exists(archive_path) or os.path.isfile(archive_path) \
#                 is False:
#             return False

#         # Upload the archive to /tmp/ directory on the web server
#         filename = os.path.basename(archive_path.split("/")[-1])
#         archive_name = os.path.basename(filename.split('.')[0])
#         put(archive_path, "/tmp/{}".format(filename))

#         # Create a new folder for the archive
#         run('sudo mkdir -p /data/web_static/releases/{}/'.format(
#             archive_name))

#         # Uncompress the archive to the new version directory
#         run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
#             format(filename, archive_name))

#         # Delete the archive from the web server
#         run('sudo rm /tmp/{}'.format(filename))

#         # Move contents into the host web_static
#         run('sudo mv /data/web_static/releases/{}/web_static/* \
#             /data/web_static/releases/{}/'.format(archive_name,
#                                                   archive_name))

#         # Delete web_static compressed directory & files
#         run('sudo rm -rf /data/web_static/releases/{}/web_static'.
#             format(archive_name))

#         # Delete the symbolic link from the web server
#         run('sudo rm -rf /data/web_static/current')
# #
#         # # Create a new symbolic link
#         run('sudo ln -sf /data/web_static/releases/{}/ \
#             /data/web_static/current'.format(archive_name))
#     except:
#         return False

#     return True
    try:
        if not os.path.exists(archive_path):
            return False
        # upload archive
        put(archive_path, '/tmp/')

        # create target dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/\
            releases/web_static_{}/'.format(timestamp))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
            /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/\
            web_static_{}/web_static/* /data/web_static/releases/\
                web_static_{}/'.format(timestamp, timestamp))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/\
            web_static_{}/web_static'
            .format(timestamp))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/\
            web_static_{}/ /data/web_static/current'.format(timestamp))
        return True
        
    except:
        return False

    # return True on success
