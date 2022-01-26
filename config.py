OPERATING_SYSTEMS = [
    {"name": "Ubuntu",
    "versions": ["18","20","17"]
    },

    {"name": "Debian",
    "versions": ["8","9","10"]
    }
]

NECESSARY_PACKAGES = ['python','sudo','rsync','ntpdate','openssh-server','debootstrap']
NICE_PACKAGES = ['tcpflow','tcpdump','nmap','netstat','htop']
REPOS = [{"url": "ftp.debian.org", "port": "80"}, {"url": "httpredir.debian.org", "port": "80"}]

