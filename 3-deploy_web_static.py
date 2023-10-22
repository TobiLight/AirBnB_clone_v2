#!/usr/bin/python3
# File: 3-deploy_web_static.py
# Author: Oluwatobiloba Light
"""Fabric script that creates and distributes an archive to your web servers"""
from fabric.api import run, put, env, local, runs_once, task
from datetime import datetime
import os


env.hosts = ['204.236.240.195', '34.239.253.9']


@runs_once
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

        print("Packing web_static to {}".format(filename))
        # Create the archive
        archive = local(
            'tar -czvf {} web_static'.format(filename))
        # Check if the archive creation failed
        if archive.failed is True:
            return None
        print("web_static packed: {} -> {}Bytes"
              .format(filename, os.path.getsize(filename=filename)))
        return filename
    except Exception as e:
        return None
    # formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    # mkdir = "mkdir -p versions"
    # path = "versions/web_static_{}.tgz".format(formatted_dt)
    # print("Packing web_static to {}".format(path))
    # if local("{} && tar -cvzf {} web_static".format(mkdir, path)).succeeded:
    #     return path
    # return None


@task
def do_deploy(archive_path):
    """
    Distribute an archive to web servers.
    """
    try:
        if not os.path.exists(archive_path) or os.path.isfile(archive_path) \
                is False:
            return False

        # Upload the archive to /tmp/ directory on the web server
        filename = os.path.basename(archive_path.split("/")[-1])
        archive_name = os.path.basename(filename.split('.')[0])
        dir_path = "/data/web_static/releases/"

        # Upload file to remote server
        put(archive_path, "/tmp/")

        # run("sudo rm -rf {}{}/".format(dir_path, archive_name))
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
        # # Create a new symbolic link
        run('sudo ln -s {}{}/ \
            /data/web_static/current'.format(dir_path, archive_name))
        print("New version deployed!")
        return True
    except Exception:
        return False
    # try:
    #     if not os.path.exists(archive_path):
    #         return False
    #     fn_with_ext = os.path.basename(archive_path)
    #     fn_no_ext, ext = os.path.splitext(fn_with_ext)
    #     dpath = "/data/web_static/releases/"
    #     put(archive_path, "/tmp/")
    #     # run("rm -rf {}{}/".format(dpath, fn_no_ext))
    #     run("mkdir -p {}{}/".format(dpath, fn_no_ext))
    #     run("tar -xzf /tmp/{} -C {}{}/"
    #         .format(fn_with_ext, dpath, fn_no_ext))
    #     run("rm /tmp/{}".format(fn_with_ext))
    #     run("mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))
    #     run("rm -rf {}{}/web_static".format(dpath, fn_no_ext))
    #     run("rm -rf /data/web_static/current")
    #     run("ln -s {}{}/ /data/web_static/current".format(dpath, fn_no_ext))
    #     print("New version deployed!")
    #     return True
    # except Exception:
    #     return False


@task
def deploy():
    """Creates and distributes an archive to your web servers"""
    file_archive = do_pack()
    if file_archive is None:
        return False
    return do_deploy(file_archive)
