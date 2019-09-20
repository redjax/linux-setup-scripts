"""
Handles the various package managers and their functions.
"""


class LinuxDistro:
    """Class to create distro-specific instances."""

    def __init__(self, name, packageMgr):
        # Distribution name, i.e. "fedora"
        self.name = name
        # Distribution's package manager, i.e. "dnf"
        self.packageMgr = packageMgr

    def packageCommands(self, packageMgr, command):
        """Build commands list for package manager."""
        # May be unnecessary repetition
        self.packageMgr = packageMgr
        # Returns package manager's command, i.e. "dnf"
        self.command = command

    def returnDistro(self):
        # Return the instance's distribution name
        return self.name

    def returnPkgMgr(self):
        # Return the instance's package manager command
        return self.packageMgr


class PackageMgr:
    """Functions related to a distribution's package manager."""
    def __init__(self, command, update, install, remove, search, noconfirm):
        # Package manager's command to update packages
        self.update = update
        # Command to install packages
        self.install = install
        # Command to remove/uninstall packages
        self.remove = remove
        # Command to search repositories
        self.search = search
        # Command to skip confirmation, i.e. "-y"
        self.noconfirm = noconfirm

    def installPkg(self, command, package):
        """Build the command to install a package and return it."""
        # Build the package manager-specific install command
        cmd = "{} {} {} {}".format(command, self.install, self.noconfirm,
                                   package)
        # Return the command when this function is run
        return cmd

    def removePkg(self, command, package):
        """Build the command to remove a package and return it."""
        # Build package manager-specific remove command
        cmd = "{} {} {} {}".format(command, self.remove, self.noconfirm,
                                   package)
        return cmd

    def searchPkg(self, command, package):
        """Build the command to search for a package and return it."""
        cmd = "{} {} {}".format(command, self.search, package)
        return cmd
