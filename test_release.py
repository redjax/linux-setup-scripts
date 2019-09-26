import subprocess

# Shell command to get release information
release_cmd = ['lsb_release', '-a']
test_cmd = ['ls', '-a', '/home/jack/']


def write_to_file(file, data, optype='w+'):
    """Write data to a file. Default optype is w+"""
    # Open file as optype (i.e. r, w, w+, etc)
    outfile = open(file, optype)
    # Write passed data to the file
    outfile.write(data)
    # Close file
    outfile.close()


def test_runcmd(cmd, outfile):
    """Test function for running shell commands."""
    # Build shell command
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               shell=False)

    # Get output of command in variable
    output = process.stdout.read().decode()

    write_to_file('this_pc/testout.txt', 'w+', output)


def find_distro_info(file, search_term):
    """Find related information from text file.
    TODO: Break out each search item into new function
    for easier development/variable creation."""
    # Open file passed as arg for reading
    searchfile = open(file, 'r')
    # Loop through file to find search_term
    for line in searchfile:
        if search_term in line:
            return line
    searchfile.close()


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
    distributor = find_distro_info('this_pc/testout.txt', 'Distributor ID:')
    # Create release object
    release = find_distro_info('this_pc/testout.txt', 'Release:')
    # Create codename object
    codename = find_distro_info('this_pc/testout.txt', 'Codename:')
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

    test_runcmd(release_cmd, 'this_pc/testout.txt')
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
    return output


# test_commands()
print(test_better_release())
