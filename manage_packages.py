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


"""FEDORA"""
# Class instance for Fedora.
fedora = LinuxDistro("fedora", "dnf")
# The DNF package manager
pkgrDNF = LinuxDistro.returnPkgMgr(fedora)
# Build DNF commands
buildDNF = PackageMgr(pkgrDNF, "upgrade", "install", "remove", "search", "-y")

"""Ubuntu"""
# Class instance for Ubuntu
ubuntu = LinuxDistro("ubuntu", "apt")
# The apt package manager
pkgrAPT = LinuxDistro.returnPkgMgr(ubuntu)
# Build APT commands
buildAPT = PackageMgr(pkgrAPT, "update", "install", "remove",
                      "cache search", "-y")

"""Test DNF commands"""
testDnfInstall = buildDNF.installPkg(pkgrDNF, "screen")
testDnfRemove = buildDNF.removePkg(pkgrDNF, "screen")
testDnfSearch = buildDNF.searchPkg(pkgrDNF, "screen")

"""Test APT commands"""
testAptInstall = buildAPT.installPkg(pkgrAPT, "screen")
testAptRemove = buildAPT.removePkg(pkgrAPT, "screen")
testAptSearch = buildAPT.searchPkg(pkgrAPT, "screen")


def testPrint(distro, install, remove, search):
    print("{} {} {}\n".format(distro, "install command test: \n", install))
    print("{} {} {}\n".format(distro, "remove command test: \n", remove))
    print("{} {} {}\n".format(distro, "search command test: \n", search))


testPrint("Fedora", testDnfInstall, testDnfRemove, testDnfSearch)
testPrint("Ubuntu", testAptInstall, testAptRemove, testAptSearch)
