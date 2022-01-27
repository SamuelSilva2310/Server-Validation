
USER = "samuel"
OPERATING_SYSTEMS = [{"name": "Ubuntu", "versions": ["18","20","17"]}, {"name": "Debian", "versions": ["8","9","10"]}]
NECESSARY_PACKAGES = ['python','sudo','rsync','ntpdate','openssh-server','debootstrap']
NICE_PACKAGES = ['tcpflow','tcpdump','nmap','netstat','htop']
REPOS = [{"url": "ftp.debian.org", "port": "80"}, 
        {"url": "httpredir.debian.org", "port": "2500"},
        {"url": "ftp-master.debian.org", "port": "80"}]

SERVERS = [{
        "user": "root", 
        "key":"/root/.ssh/id_rsa", 
        "ip": ["104.248.203.245", "axess311.axiros.kjoo.net","axess5.axiros.kjoo.net"]}]