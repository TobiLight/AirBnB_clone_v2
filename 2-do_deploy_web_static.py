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
        # filename = os.path.basename(archive_path.split("/")[-1])
        # archive_name = os.path.basename(filename.split('.')[0])
        if not os.path.exists(archive_path) or os.path.isfile(archive_path) \
                is False:
            return False

        # Upload the archive to /tmp/ directory on the web server
        filename = os.path.basename(archive_path.split("/")[-1])
        archive_name = os.path.basename(filename.split('.')[0])
        put(archive_path, "/tmp/{}".format(filename))

        # Create a new folder for the archive
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(
            archive_name))

        # Uncompress the archive to the new version directory
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
            format(filename, archive_name))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(filename))

        # Move contents into the host web_static
        run('sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(archive_name,
                                                  archive_name))

        # Delete web_static compressed directory & files
        run('sudo rm -rf /data/web_static/releases/{}/web_static'.
            format(archive_name))

        # Delete the symbolic link from the web server
        run('sudo rm -rf /data/web_static/current')
#
        # # Create a new symbolic link
        run('sudo ln -sf /data/web_static/releases/{}/ \
            /data/web_static/current'.format(archive_name))
        # print("New version deployed!")
        return True
    except Exception:
        return False

    # try:
    #     if not os.path.exists(archive_path):
    #         return False
    #     fn_with_ext = os.path.basename(archive_path)
    #     fn_no_ext, ext = os.path.splitext(fn_with_ext)
    #     dpath = "/data/web_static/releases/"
    #     # put(archive_path, "/tmp/")
    #     print(put('versions/web_static_202310621927.tgz', "/tmp/"))
    #     print("New version deployed!")
    #     run("sudo rm -rf {}{}/".format(dpath, fn_no_ext))
    #     run("sudo mkdir -p {}{}/".format(dpath, fn_no_ext))
    #     run("sudo tar -xzf /tmp/{} -C {}{}/".format(fn_with_ext, dpath, fn_no_ext))
    #     run("sudo rm /tmp/{}".format(fn_with_ext))
    #     run("sudo mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))
    #     run("sudo rm -rf {}{}/web_static".format(dpath, fn_no_ext))
    #     run("sudo rm -rf /data/web_static/current")
    #     run("sudo ln -s {}{}/ /data/web_static/current".format(dpath, fn_no_ext))
        
    #     return True
    # except Exception:
    #     return False