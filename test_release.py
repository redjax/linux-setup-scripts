import subprocess

import sysops

# Shell command to get release information
release_cmd = ['lsb_release', '-a']
test_cmd = ['ls', '-a', '/home/jack/']


def build_pc_info_file(file, data):
    """Build a json file with data found about current PC."""
    # data = {
    #     'os': "",
    #     'distro': "",
    #     'release': "",
    #     'codename': ""
    # }

    # write_to_file(file, output)


def test_releaseinfo():
    """Get text from release info file, strip down to essential info."""
    # List of words to scan string for, then remove
    remove_words_list = ['Distributor',
                         'ID:',
                         ' ',
                         'Release:',
                         'Codename:',
                         '\t']

    # Create distributor object
    distributor = sysops.find_line_in_file('this_pc/testout.txt',
                                           'Distributor ID:')
    # Create release object
    release = sysops.find_line_in_file('this_pc/testout.txt', 'Release:')
    # Create codename object
    codename = sysops.find_line_in_file('this_pc/testout.txt', 'Codename:')

    # Next 3 lines create objects to be stripped of remove_words_list items
    distributor_cleaned = distributor.split()
    release_cleaned = release.split()
    codename_cleaned = codename.split()

    # Strip words from remove_words_list out of input text
    distributor_result = [word for word in distributor_cleaned
                          if word not in remove_words_list]
    release_result = [word for word in release_cleaned
                      if word not in remove_words_list]
    codename_result = [word for word in codename_cleaned
                       if word not in remove_words_list]

    return distributor_result[0], release_result[0], codename_result[0]


def test_commands():
    """Function to run each command as a test."""
    release_cmd = ['lsb_release', '-a']

    sysops.run_cmd(release_cmd, 'this_pc/testout.txt')
    print(test_releaseinfo())


def test_better_release():
    """Test the better version of LSB command.

    This command gets the distro and release number in a more concise way than
    my release_info functions. It simply returns OS+version
    (i.e. Ubuntu 19.04).

    Full command:
    lsb_release -ds 2>/dev/null || cat /etc/*release 2>/dev/null | head -n1 \
        || uname -om
    """
    # Split full command into 4 parts
    cmd_pt1 = "lsb_release -ds 2>/dev/null"
    cmd_pt2 = "cat /etc/*release 2>/dev/null"
    cmd_pt3 = "head -n1"
    cmd_pt4 = "uname -om"
    # Assemble parts into full command
    cmd = cmd_pt1 + ' || ' + cmd_pt2 + ' | ' + cmd_pt3 + ' || ' + cmd_pt4

    # Run command and pipe output
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               shell=True)

    # Get output of command in variable
    output = process.stdout.read().decode()
    distro, release = output.split(' ')
    # return output
    print("Distribution: {}\nRelease: {}".format(distro, release))


release_cmd = ['lsb_release', '-a']
# print(sysops.run_cmd(release_cmd))
print(sysops.find_line_in_file('this_pc/testout.txt', "Distributor ID:"))
