#!/usr/bin/python3
# File: 100-clean_web_static.py
# Author: Oluwatobiloba Light
"""Fabric script that deletes out-of-date archives"""
from fabric.api import *
import os

env.hosts = ['204.236.240.195', '52.91.123.82	']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, it keeps only the most recent archive. If
    number is 2, it keeps the most and second-most recent archives.
    """
    if int(number) == 0:
        number = 1
    else:
        number = int(number)
    
    archives = sorted(os.listdir("versions"))
    for i in range(number):
        archives.pop()
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        for a in archives:
            if 'web_static_' in a:
                archives = a
        for i in range(number):
            archives.pop()
        for a in archives:
            run('rm -rf ./{}'.format(a))
