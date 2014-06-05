import os
import subprocess

import getpass
"""Does the necessary leg work to install SSHTunnel dependencies on Debian-based systems

THIS SCRIPT IS INCLUDED IN post_inst for debian packages

"""


"""This block can be taken care of with apt-get install
os.chdir("tsocks-1.8/")
dir_of_tsocks = os.getcwd()

LOGNAME = getpass.getuser() # LINUX DEPENDANT, LOGNAME is the current user
subprocess.check_call(["./configure", "--with-conf='/home/' + LOGNAME + '.local/share'"]) #Configure
subprocess.check_call(["make"]) #Compile


"""
tsocks_text = """
# This is the configuration for libtsocks (transparent socks)
# Lines beginning with # and blank lines are ignored
#
# The basic idea is to specify:
#	- Local subnets - Networks that can be accessed directly without
#			  assistance from a socks server
#	- Paths - Paths are basically lists of networks and a socks server
#		  which can be used to reach these networks
#	- Default server - A socks server which should be used to access 
#			   networks for which no path is available
# Much more documentation than provided in these comments can be found in
# the man pages, tsocks(8) and tsocks.conf(8)

# Local networks
# For this example this machine can directly access 192.168.0.0/255.255.255.0 
# (192.168.0.*) and 10.0.0.0/255.0.0.0 (10.*)

local = 192.168.0.0/255.255.255.0
local = 10.0.0.0/255.0.0.0

# Paths
# For this example this machine needs to access 150.0.0.0/255.255.0.0 as 
# well as port 80 on the network 150.1.0.0/255.255.0.0 through
# the socks 5 server at 10.1.7.25 (if this machines hostname was 
# "socks.hello.com" we could also specify that, unless --disable-hostnames
# was specified to ./configure).

path {
	reaches = 150.0.0.0/255.255.0.0
	reaches = 150.1.0.0:80/255.255.0.0
	server = 10.1.7.25
	server_type = 5
	default_user = delius
	default_pass = hello
}

# Default server
# For connections that aren't to the local subnets or to 150.0.0.0/255.255.0.0
# the server at 192.168.0.1 should be used (again, hostnames could be used
# too, see note above)

server = 127.0.0.1
# Server type defaults to 4 so we need to specify it as 5 for this one
server_type = 5
# The port defaults to 1080 but I've stated it here for clarity 
server_port = 1080"""

print("Installing, please be patient")
print("If the installation fails you should install 'tsocks' and 'python3-pyside', and replace the /etc/tsocks.conf file with the one provided, provided here for your convienience: \n" + tsocks_text)
subprocess.call(["apt-get", "install", "-y", "tsocks","python3-pyside"],stdout=open(os.devnull,'wb'))

#Modify config file
config = open('/etc/tsocks.conf','w')


config.write(tsocks_text)
config.close()

