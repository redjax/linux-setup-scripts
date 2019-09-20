from setupScriptClasses import LinuxDistro as LinuxDistro
from setupScriptClasses import PackageMgr as PackageMgr

"""Fedora"""
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

"""Arch"""
arch = LinuxDistro("arch", "pacman")
pkgrPacman = LinuxDistro.returnPkgMgr(arch)
buildPacman = PackageMgr(pkgrPacman, "-Syu", "-S", "-Rnf",
                         "-Ss", "--noconfirm")

"""Test DNF commands"""
testDnfInstall = buildDNF.installPkg(pkgrDNF, "screen")
testDnfRemove = buildDNF.removePkg(pkgrDNF, "screen")
testDnfSearch = buildDNF.searchPkg(pkgrDNF, "screen")

"""Test APT commands"""
testAptInstall = buildAPT.installPkg(pkgrAPT, "screen")
testAptRemove = buildAPT.removePkg(pkgrAPT, "screen")
testAptSearch = buildAPT.searchPkg(pkgrAPT, "screen")

"""Test PACMAN commands"""
testPacmanInstall = buildPacman.installPkg(pkgrPacman, "screen")
testPacmanRemove = buildPacman.removePkg(pkgrPacman, "screen")
testPacmanSearch = buildPacman.searchPkg(pkgrPacman, "screen")


def testPrint(distro, install, remove, search):
    print("{} {} {}\n".format(distro, "install command test: \n", install))
    print("{} {} {}\n".format(distro, "remove command test: \n", remove))
    print("{} {} {}\n".format(distro, "search command test: \n", search))


testPrint("Fedora", testDnfInstall, testDnfRemove, testDnfSearch)
testPrint("Ubuntu", testAptInstall, testAptRemove, testAptSearch)
testPrint("Arch", testPacmanInstall, testPacmanRemove, testPacmanSearch)
