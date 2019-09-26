"""Creates and runs scripts & commands for various Linux distros.

I've generally already created scripts for installing applications from repos,
moving configuration files around the file system, etc. This script is intended
to orchestrate all that, and hopefully add more flexibility.
"""
import json

# Import subprocess for running commands concurrently
import sysops

# Import classes from setupScriptClasses.py
# from setupScriptClasses import LinuxDistro as LinuxDistro
# from setupScriptClasses import PackageMgr as PackageMgr


def get_distro_release():
    """Test the better version of LSB command.

    This command gets the distro and release number in a more concise way than
    my release_info functions. It simply returns OS+version
    (i.e. Ubuntu 19.04).
    """
    # Split full command into 4 parts
    cmd_pt1 = "lsb_release -ds 2>/dev/null"
    cmd_pt2 = "cat /etc/*release 2>/dev/null"
    cmd_pt3 = "head -n1"
    cmd_pt4 = "uname -om"
    # Assemble parts into full command
    cmd = cmd_pt1 + ' || ' + cmd_pt2 + ' | ' + cmd_pt3 + ' || ' + cmd_pt4

    # Run command and pipe output
    output = sysops.run_cmd(cmd, shelltype=True)

    distro, release = output.split(' ')
    return distro, release


def update_system_info(file, distro, release):
    """Write distribution and release to system_info.json"""
    writedata = {'distro': distro, 'release': release.strip('\n')}

    with open(file, 'w') as jsonfile:
        json.dump(writedata, jsonfile)


def prep_release_info(file):
    """Prepare data to write distribution & release info to system_info.json"""
    distro, release = get_distro_release()

    update_system_info(file, distro, release)


def read_release_info(file, mode='r'):
    """Read release info from system_info.json"""
    with open(file, mode) as f:
        data = json.load(f)

        distro = data['distro']
        release = data['release']

        return distro, release


tmp_file = 'this_pc/system_info.json'
prep_release_info(tmp_file)
print(read_release_info(tmp_file))
