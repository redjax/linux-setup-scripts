#!/bin/bash
# Script found on xsuchy's fedora-upgrade Github repo: https://github.com/xsuchy/fedora-upgrade
# vim: sw=3:ts=3:et
set -e

FEDORA_VERSION=$(rpm -q --qf '%{version}' fedora-release)
TARGET_VERSION=$((FEDORA_VERSION + 1))
UPGRADE_FINISHED=0

function check_installation() {
  [[ -e /usr/sbin/fedora-upgrade ]]
}

function pause() {
   # clear the stdin buffer and pause with question
   read -t 1 -n 10000 discard || [ $? -gt 128 ]
   read -p "Hit Enter to continue or Ctrl + C to cancel."
}

function continue_or_skip() {
   read -t 1 -n 10000 discard || [ $? -gt 128 ]
   echo -e $1
   echo "This step is highly recommended, but can be safely skipped."
   ANSWER='XXX'
   while [ "$ANSWER" != "" -a "$ANSWER" != "S" ] ; do
     read -p "Hit Enter to continue, Ctrl + C to cancel or S + Enter to skip. " ANSWER
     ANSWER=$(echo $ANSWER | tr "[:lower:]" "[:upper:]")
   done
}

function dnf_install_deps() {
  # TODO add -q to all dnf and create some kind of progress meter
  # but now be verbose
  install_if_missing rpmconf
  install_if_missing dnf-plugins-core
}

function install_if_missing() {
  echo "Checking if $1 is installed."
  rpm -q $1 >/dev/null || dnf install -y -q $1
}

function upgrade_before_upgrade() {
  continue_or_skip "\nGoing to run 'dnf upgrade' before upgrading."
  if [ "$ANSWER" != "S" ] ; then
    dnf upgrade
  fi
}

function dnf_upgrade_before_upgrade() {
  continue_or_skip "\nGoing to run 'dnf upgrade' before upgrading."
  if [ "$ANSWER" != "S" ] ; then
    dnf upgrade
  fi
}

function rpmconf_before_upgrade() {
  continue_or_skip "\nGoing to resolve old .rpmsave and .rpmnew files before upgrading."
  if [ "$ANSWER" != "S" ] ; then
    rpmconf -fvimdiff -a
  fi
}

function import_keys() {
  echo "Importing new RPM-GPG keys."
  rpm --import /usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-$TARGET_VERSION-primary
  if [ -f /etc/yum.repos.d/rpmfusion-free.repo -a -e /usr/share/distribution-gpg-keys/rpmfusion/RPM-GPG-KEY-rpmfusion-free-fedora-$TARGET_VERSION ]; then
    rpm --import /usr/share/distribution-gpg-keys/rpmfusion/RPM-GPG-KEY-rpmfusion-free-fedora-$TARGET_VERSION
  fi
  if [ -f /etc/yum.repos.d/rpmfusion-nonfree.repo -a -e /usr/share/distribution-gpg-keys/rpmfusion/RPM-GPG-KEY-rpmfusion-nonfree-fedora-$TARGET_VERSION ]; then
    rpm --import /usr/share/distribution-gpg-keys/rpmfusion/RPM-GPG-KEY-rpmfusion-nonfree-fedora-$TARGET_VERSION
  fi
}

function install_base() {
  continue_or_skip "\nGoing to install missing packages from group 'Minimal Install'"
  if [ "$ANSWER" != "S" ] ; then
    dnf group install 'Minimal Install'
  fi
}

function dnf_install_base() {
  continue_or_skip "\nGoing to install missing packages from group 'Minimal Install'"
  if [ "$ANSWER" != "S" ] ; then
    dnf groupupdate 'Minimal Install'
  fi
}

function rpmconf_after_upgrade() {
  continue_or_skip "\nGoing to resolve .rpmsave and .rpmnew files after upgrade."
  if [ "$ANSWER" != "S" ] ; then
    rpmconf -fvimdiff -a
    rpmconf --clean
  fi
}

function reset_service_priorities() {
  continue_or_skip "\nGoing to resets all installed unit files to the defaults configured\nin the preset policy file."
  if [ "$ANSWER" != "S" ] ; then
    systemctl preset-all
  fi
}

function cleanup_cache() {
  rm -rf /var/cache/yum/* /var/cache/dnf/* /var/cache/PackageKit/*
}

function unwanted_packages() {
  LAST=$1
  continue_or_skip "\nThere may be some packages which are now orphaned, do you want to see them?"
  RESULT=0
  package-cleanup --orphans | grep -v kernel && RESULT=1
  if [ 0$RESULT -eq 1 ]; then
    echo "These packages are very probably orphaned. You may want to remove them."
  fi
}

function is_prerelease() {
  # will print string "--enablerepo=updates-testing" if this is prerelease, "" otherwise
  local RELEASE=$1
  TEMP=$(mktemp -d)
  dnf download -q --destdir "$TEMP" --disablerepo=* --enablerepo=fedora --releasever=$RELEASE fedora-repos
  if rpm2cpio "$TEMP"/fedora-repos*.rpm | cpio -i --quiet --to-stdout - ./etc/yum.repos.d/fedora-updates-testing.repo | grep 'enabled=1' >/dev/null ; then
    echo "--enablerepo=updates-testing"
  else
    echo ""
  fi
  rm -rf "$TEMP"
}

function print_exit_banner() {
  if [ $UPGRADE_FINISHED -eq 1 ]; then
    echo
    echo You successfully upgraded to Fedora $TARGET_VERSION
    echo Reboot is strongly suggested.
    exit 0
  elif [ $UPGRADE_FINISHED -eq 0 ]; then
    echo
    echo Upgrade to Fedora $TARGET_VERSION was not finished!
    echo You can safely re-run fedora-upgrade again to start over.
    exit 1
  else
    echo
    echo Upgrade to Fedora $TARGET_VERSION was not finished!
    echo Finish steps manually according to documentation on the wiki:
    echo 'https://fedoraproject.org/wiki/Upgrading_Fedora_using_package_manager?rd=Upgrading_Fedora_using_yum#5._Make_sure_Fedora_is_upgraded'
    exit 2
  fi
}

function welcome_banner() {
  echo "Going to upgrade your Fedora to version $1."
  echo "You may want to read Release Notes:"
  echo "  http://docs.fedoraproject.org/f${TARGET_VERSION}/release-notes/"
  pause
}

function warn_about_online() {
  echo "Warning: This is unofficial upgrade path. For official tool see:"
  echo "         https://fedoraproject.org/wiki/Upgrading"
  echo "         While author of fedora-upgrade thinks online upgrade is better, it is"
  echo "         not officially tested by FedoraQA."
  pause
}

function going_to_reboot() {
  echo ""
  echo "********** End of DNF plugin output **********"
  echo ""
  echo "Download complete! The downloaded packages were saved in cache till the next"
  echo "successful transaction. You can remove cached packages by executing"
  echo "'dnf clean packages'."
  echo "In next step your computer will be REBOOTED and packages will be upgraded."
  pause
}

function choose_upgrade_method() {
  echo "Choose upgrade method"
  echo "  * offline - this use dnf-plugin-system-upgrade plugin and requires two reboots"
  echo "            - this is official upgrade method"
  echo "  * online  - this use distro-sync and require only one reboot"
  echo "            - this is not offically tested by FedoraQA"
  echo "For more information see https://fedoraproject.org/wiki/Upgrading"
  read -t 1 -n 10000 discard || [ $? -gt 128 ]
}

if ! check_installation; then
  echo "Please install fedora-upgrade package using dnf first"
  exit 2
fi

if [ 0$UID -ne 0 ]; then
   echo "Error: You must be a root."
   echo "Run as: sudo fedora-upgrade"
   exit 1
fi

# make obvious ending for inexperienced users
trap "print_exit_banner" SIGHUP SIGINT SIGTERM

if [ 0$FEDORA_VERSION -eq 27 ]; then
# Fedora 27 to 28
  UPGRADE_TO=28
  welcome_banner $UPGRADE_TO

  dnf_install_deps
  dnf_upgrade_before_upgrade
  rpmconf_before_upgrade
  import_keys

  dnf clean -q dbcache metadata
  echo "Checking if this is pre-release"
  enable_updates=$(is_prerelease $UPGRADE_TO )

  choose_upgrade_method
  echo -e $1
  ANSWER='XXX'
  while [ "$ANSWER" != "offline" -a "$ANSWER" != "online" ] ; do
    read -p "What is your choice? (offline/online)  " ANSWER
    ANSWER=$(echo $ANSWER | tr "[:upper:]" "[:lower:]")
  done
  if [ "$ANSWER" == "online" ] ; then
    dnf --releasever=$UPGRADE_TO --setopt=deltarpm=false $enable_updates distro-sync
  elif [ "$ANSWER" == "offline" ] ; then
    install_if_missing dnf-plugin-system-upgrade
    dnf system-upgrade download --releasever=$UPGRADE_TO
    going_to_reboot
    dnf system-upgrade reboot
  fi
  UPGRADE_FINISHED=2

  dnf_install_base

  cleanup_cache
  rpmconf_after_upgrade
  reset_service_priorities
  unwanted_packages
  UPGRADE_FINISHED=1
elif [ 0$FEDORA_VERSION -eq 26 ]; then
# Fedora 26 to 27
  UPGRADE_TO=27
  welcome_banner $UPGRADE_TO

  dnf_install_deps
  dnf_upgrade_before_upgrade
  rpmconf_before_upgrade
  import_keys

  dnf clean -q dbcache metadata
  echo "Checking if this is pre-release" 
  enable_updates=$(is_prerelease $UPGRADE_TO )

  choose_upgrade_method
  echo -e $1
  ANSWER='XXX'
  while [ "$ANSWER" != "offline" -a "$ANSWER" != "online" ] ; do
    read -p "What is your choice? (offline/online)  " ANSWER
    ANSWER=$(echo $ANSWER | tr "[:upper:]" "[:lower:]")
  done
  if [ "$ANSWER" == "online" ] ; then
    dnf --releasever=$UPGRADE_TO --setopt=deltarpm=false $enable_updates distro-sync
  elif [ "$ANSWER" == "offline" ] ; then
    install_if_missing dnf-plugin-system-upgrade
    dnf system-upgrade download --releasever=$UPGRADE_TO
    going_to_reboot
    dnf system-upgrade reboot
  fi
  UPGRADE_FINISHED=2

  dnf_install_base

  cleanup_cache
  rpmconf_after_upgrade
  reset_service_priorities
  unwanted_packages
  UPGRADE_FINISHED=1
elif [ 0$FEDORA_VERSION -eq 28 ]; then
# Fedora 28 to rawhide
  echo "Going to upgrade your Fedora to rawhide."
  echo "Fedora $TARGET_VERSION is currently under development."
  echo "Are you sure?"
  pause

  dnf_install_deps
  rpmconf_before_upgrade

  install_if_missing fedora-repos-rawhide
  dnf config-manager --set-disabled fedora updates updates-testing
  dnf config-manager --set-enabled rawhide
  dnf upgrade -y dnf
  dnf clean -q dbcache metadata
  choose_upgrade_method
  echo -e $1
  ANSWER='XXX'
  while [ "$ANSWER" != "offline" -a "$ANSWER" != "online" ] ; do
    read -p "What is your choice? (offline/online)  " ANSWER
    ANSWER=$(echo $ANSWER | tr "[:upper:]" "[:lower:]")
  done
  if [ "$ANSWER" == "online" ] ; then
    dnf --releasever=rawhide --setopt=deltarpm=false distro-sync --nogpgcheck
  elif [ "$ANSWER" == "offline" ] ; then
    install_if_missing dnf-plugin-system-upgrade
    dnf system-upgrade download --releasever=rawhide --nogpgcheck
    going_to_reboot
    dnf system-upgrade reboot
  fi
  UPGRADE_FINISHED=2

  dnf_install_base

  cleanup_cache
  rpmconf_after_upgrade
  reset_service_priorities
  unwanted_packages
  UPGRADE_FINISHED=1
else
  echo Upgrading from version $FEDORA_VERSION is not supported.
  exit 1
fi
print_exit_banner
