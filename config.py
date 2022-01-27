
USER = "samuel"
OPERATING_SYSTEMS = [{"name": "Ubuntu", "versions": ["18","20","17"]}, {"name": "Debian", "versions": ["8","9","10"]}]
NECESSARY_PACKAGES = ['python','sudo','rsync','ntpdate','openssh-server','debootstrap']
NICE_PACKAGES = ['tcpflow','tcpdump','nmap','netstat','htop']
REPOS = [{"url": "ftp.debian.org", "port": "80"}, 
        {"url": "httpredir.debian.org", "port": "80"},
        {"url": "security.debian.org", "port": "80"},
        {"url": "archive.debian.org", "port": "80"},
        {"url": "deb.debian.org", "port": "80"},
        {"url": "keyserver.ubuntu.com", "port": "80"},
        {"url": "ftp-master.debian.org", "port": "80"}]

