"""Sysops script houses functions that perform
tasks like running shell commands and returning output,
writing objects to a file, and other system tasks."""
import pickle
import subprocess


def run_cmd(cmd, shelltype=False):
    """Test function for running shell commands."""
    # Build shell command
    process = subprocess.Popen(cmd,
                               shell=shelltype,
                               stdout=subprocess.PIPE)

    # Get output of command in variable
    output = process.stdout.read().decode()

    return output


def write_to_file(file, data, optype='w+'):
    """Write data to a file. Default optype is w+"""
    # Open file as optype (i.e. r, w, w+, etc)
    outfile = open(file, optype)
    # Write passed data to the file
    outfile.write(data)
    # Close file
    outfile.close()


def find_line_in_file(file, search_term, mode='r'):
    """Find related information from text file.
    TODO: Break out each search item into new function
    for easier development/variable creation."""
    # Open file passed as arg for reading
    searchfile = open(file, mode)
    # Loop through file to find search_term
    for line in searchfile:
        if search_term in line:
            return line
    searchfile.close()


def write_pickle():
    pass


def read_pickle():
    pass


def create_class_instance():
    """Create an instance of a class. Input must contain
    all items to be passed into new class instance."""
