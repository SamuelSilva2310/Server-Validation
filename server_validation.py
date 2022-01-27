import os
import subprocess
import platform
import distro
import pwd

import nmap
from urllib.request import urlopen

import config
from message import Message

def new_test(passed, message):
    return {"passed": passed, "message":message}




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

        devnull = open(os.devnull,"w")
        retval = subprocess.call(["dpkg","-s",package],stdout=devnull,stderr=subprocess.STDOUT)
        devnull.close()
        
        passed = retval == 0        
        results.append(new_test(passed,package))
    
    return results

def validate_user(user):
    """Validates if user exists in system

    Args:
        user (str): username

    Returns:
        bool: bool describing if the user exists or not
    """
    results = []
    filename = f"/etc/sudoers.d/{user}"
    # filename = f"{user}.txt"
    if os.path.exists(filename):

        passed_file_exists = True
        with open(filename,"r") as f:
            content = f.read()
            wanted_content = f"{user} ALL=(ALL) NOPASSWD:ALL"
            passed_content = content == wanted_content
    else:
        passed_file_exists = False
        passed_content = False

    results.append(new_test(passed_file_exists, "User File Exists"))
    results.append(new_test(passed_content, f"Sudoers User File Content ({user} ALL=(ALL) NOPASSWD:ALL)"))
    
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
            results.append(new_test(True,repo['url']))
        else:
            results.append(new_test(False,repo['url']))
    return results


    

    
def build_response():

    message = Message()
    # Validade the OS
    message.add_section("Operating System", validate_system_os(config.OPERATING_SYSTEMS))


    # Validade Packages

    # Necessary Packages
    message.add_section("Necessadry packages", validate_packages(config.NECESSARY_PACKAGES))
    # Nice to have Packages
    message.add_section("Nice To Have packages", validate_packages(config.NICE_PACKAGES))


    
    # Validade User exists
    message.add_section("Sudoers User", validate_user(config.USER))


    # Validate repo apt servers
    message.add_section("Connection to Repos",validate_repos(config.REPOS))


    return message.get_content()




# validate_packages("Necessary Packages", config.NECESSARY_PACKAGES)
# validate_packages("Nice Packages",config.NICE_PACKAGES)

# print(validate_system_os(config.GOOD_OS))
# validate_servers(config.SERVERS)

print(build_response())

