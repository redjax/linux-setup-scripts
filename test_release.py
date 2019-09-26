import subprocess

# Shell command to get release information
release_cmd = ['lsb_release', '-a']
test_cmd = ['ls', '-a', '/home/jack/']

# Open shell and run command, pipe output to stdout var
process = subprocess.Popen(release_cmd, stdout=subprocess.PIPE, shell=False)
# Create decoded output from stdout var
output = process.stdout.read().decode()

# Write output to text file for reading later
outfile_name = 'this_pc/testout.txt'

outfile = open(outfile_name, 'w+')
outfile.write(output)
outfile.close()


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
    data = {
        'os': "",
        'distro': "",
        'release': "",
        'codename': ""
    }

    outfile = open(file, 'w+')
    outfile.write(output)
    outfile.close()


def test_releaseinfo():
    """Get text from release info file, strip down to essential info."""
    # List of words to scan string for, then remove
    remove_words_list = ['Distributor', 'ID:', ' ', 'Release:', 'Codename:', '\t']

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
    distributor_result = [word for word in distributor_cleaned if word not in remove_words_list]
    release_result = [word for word in release_cleaned if word not in remove_words_list]
    codename_result = [word for word in codename_cleaned if word not in remove_words_list]

    return distributor_result[0], release_result[0], codename_result[0]


print(test_releaseinfo())
