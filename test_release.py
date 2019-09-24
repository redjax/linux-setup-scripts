import subprocess


def build_cmd(cmd):
    """Takes a command (cmd) passed as a list of parameters
    and returns the result."""
    result = subprocess.Popen(cmd,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    output, err = result.communicate(b"input data that is passed to subprocess' stdin")
    rc = result.returncode

    return rc


release_cmd = ['lsb_release', '-a']
test_command = ['ls', '-a', '/home/jack/Documents/git/linux-setup-scripts']

print(build_cmd(release_cmd))
