import os
import subprocess
import platform
import distro
import pwd
from paramiko import SSHClient, BadHostKeyException, AuthenticationException, SSHException, AutoAddPolicy
import socket
import nmap
from urllib.request import urlopen

import config
from message import Message


def new_test(passed, message):
    return {"passed": passed, "message": message}


def validate_system_os(operating_systems):
    """Receives a list of supported operating systems 
    and checks if the current os is suported

    Args:
        operating_systems (list): list of Dicts {} containing information about each os

    Returns:
        bool: Boolean based on if our os is supported
    """
    id = distro.id()
    version = distro.version()
    name = distro.name()
    passed = False

    for operating_system in operating_systems:
        operating_system_name = operating_system["name"].lower()

        if name.lower() == operating_system_name or id.lower() == operating_system_name:

            operating_system_versions = operating_system["versions"]
            if version.split(".")[0] in operating_system_versions:
                passed = True

    return [new_test(passed, "Operating System")]


def validate_packages(packages):
    """
    Receives a list of packages and 
    check if each one is either installed or not
    """

    results = []

    for package in packages:

        devnull = open(os.devnull, "w")
        retval = subprocess.call(
            ["dpkg", "-s", package], stdout=devnull, stderr=subprocess.STDOUT)
        devnull.close()

        passed = retval == 0
        results.append(new_test(passed, package))

    return results


def validate_user(user):
    """Validates if user exists in system

    Args:
        user (str): username

    Returns:
        bool: bool describing if the user exists or not
    """
    results = []

    try:
        if pwd.getpwnam(user):
            user_exists = True
    except KeyError:
        user_exists = False

    filename = f"/etc/sudoers.d/{user}"
    # filename = f"{user}.txt"
    if os.path.exists(filename):

        passed_file_exists = True
        with open(filename, "r") as f:
            content = f.read()
            wanted_content = f"{user} ALL=(ALL) NOPASSWD:ALL"
            passed_content = content == wanted_content
    else:
        passed_file_exists = False
        passed_content = False
    
    results.append(new_test(user_exists, f"Users '{user}' Exists"))
    results.append(new_test(passed_file_exists, f"User '{user}' Sudoers File Exists"))
    results.append(new_test(
        passed_content, f"Sudoers User File Content ({user} ALL=(ALL) NOPASSWD:ALL)"))

    return results


def validate_repos(repos):
    """Checks connection to each server

    Args:
        servers ([type]): [description]
    """
    results = []
    nmScan = nmap.PortScanner()

    for repo in repos:
        if nmScan.scan(repo['url'], repo["port"]):
            results.append(new_test(True, repo['url']))
        else:
            results.append(new_test(False, repo['url']))
    return results


def validate_shh_connections(servers):
    """Validates acess to servers using ssh

    Args:
        servers (dict): [description]
    """

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    results = []

    for server in servers:
        for ip in server['ip']:
            try:
                ssh.connect(
                    ip, username=server['user'], key_filename=server['key'])
                can_connect = True
            except (BadHostKeyException, AuthenticationException,
                    SSHException, socket.error) as e:
                can_connect = False

            results.append(new_test(can_connect, ip))

    return results


def build_response():

    message = Message()

    # Connectivity to servers
    message.add_section("Connectivity to servers",
                        validate_shh_connections(config.SERVERS))

    # Validade the OS
    message.add_section("Operating System",
                        validate_system_os(config.OPERATING_SYSTEMS))

    # Validade Packages

    # Necessary Packages
    message.add_section("Necessary packages",
                        validate_packages(config.NECESSARY_PACKAGES))
    # Nice to have Packages
    message.add_section("Nice To Have packages",
                        validate_packages(config.NICE_PACKAGES))

    # Validade User exists
    message.add_section("Sudoers User", validate_user(config.USER))

    # Validate repo apt servers
   # message.add_section("Connection to Repos", validate_repos(config.REPOS))

    return message.get_content()


# validate_shh_connections(config.SERVERS)
print(build_response())
