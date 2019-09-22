"""Creates and runs scripts & commands for various Linux distros.

I've generally already created scripts for installing applications from repos,
moving configuration files around the file system, etc. This script is intended
to orchestrate all that, and hopefully add more flexibility.
"""
# Import subprocess for running commands concurrently
import subprocess

# Import classes from setupScriptClasses.py
from setupScriptClasses import LinuxDistro as LinuxDistro
from setupScriptClasses import PackageMgr as PackageMgr


def get_linux_release():
    cmd = "lsb_release -ds 2>/dev/null || cat /etc/*release 2>/dev/null | head -n1 || uname -om"
    subprocess.call([cmd])
