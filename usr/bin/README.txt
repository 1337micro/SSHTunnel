   ___ ___ _ _ _____ _
  / __| / __| | || | |_ _| _ _ _ _ _ _ ___ | | ___ _ _ \__ \ \__ \ | __ | | | |
  +| | | ' \ | ' \ / -_) | | / -_) | '_| |___/ |___/ |_||_| _|_|_ \_,_| |_||_|
  |_||_| \___| _|_|_ \___| _|_|_
_|"""""||"""""||"""""||"""""||"""""||"""""||"""""||"""""||"""""||"""""||"""""|
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
Written by bluezone in python 3

E-mail questions and help requests to: apparentlyeverythingistaken@gmail.com


Purpose: Tunnel your browser activity or networking activity of any other
application to a remote server with ssh, in order to stay anonymous online, and
to protect yourself on potentially unsecure networks


INSTALLATION on debian-based systems: sudo python3 setup.py

you can then execute the command python3 SSHTunnel.py to run the application

INSTALLATION on other systems, or alternate installation for failed installs:
    Windows is not supported at all at this time Mac is not supported but might
    work if you follow the requirements section
    

USAGE:
    You need to have a server that allows you to ssh into it.
    
    python3 SSHTunnel.py press "I have an ssh-capable server" Enter the username
    you use to log into your server Enter the server ip Enter the ABSOLUTE PATH
    of the Key file IF you need one to login (the key file will need to be sudo
    chmod 400 in some cases, the application will not do this for you)
        If you don't need a key to login just leave it blank
        
    Press Connect Pay close attention to your terminal, you may be required to
    enter information before the application can continue IF you get an error
    message please check that your information is right and that your identity
    file has the right permissions ___ In the next window you will see the SOCKS
    proxy information, you can either enter this information manually into your
    browser settings or press one of the buttons
        to launch a special instance of the browser. WARNING, if you use the
        buttons you current firefox or chrome windows MAY BE KILLED, please save
        your work! This special instance will not change your browser's network
        settings on your main profile
    
    You can also type a terminal command to tunnel any of your favorite
    applications (especially those which don't allow you to modify proxy
    settings)
        For instance, you can type irssi to launch an instance of irssi that is
        tunneled through your ssh server
    
    
    


REQUIREMENTS:
    sudo python3 setup.py attempts to install the necessary requirements for
    debian-based distributions

    In other cases, or in cases of failed installs: 1.0) Install the following
    requirements:
        tsocks (prefer version 1.8 http://tsocks.sourceforge.net/download.php)
        python3 (prefer version 3.2+, MUST BE PYTHON 3) python3-pyside (version
        shouldn't matter)
    1.1) If it hasn't been done already, youll need to create an alias for
    tsocks, such that when you type tsocks in the terminal it will open tsocks
    
    
    2) sudo gedit /etc/tsocks.conf and replace the entire file with the
    following text:
# This is the configuration for libtsocks (transparent socks) Lines beginning
# with # and blank lines are ignored# The basic idea is to specify:
#       - Local subnets - Networks that can be accessed directly without
#                         assistance from a socks server
#       - Paths - Paths are basically lists of networks and a socks server
#                 which can be used to reach these networks
#       - Default server - A socks server which should be used to access
#                          networks for which no path is available
# Much more documentation than provided in these comments can be found in the
# man pages, tsocks(8) and tsocks.conf(8)

# Local networks For this example this machine can directly access
# 192.168.0.0/255.255.255.0 (192.168.0.*) and 10.0.0.0/255.0.0.0 (10.*)

local = 192.168.0.0/255.255.255.0 local = 10.0.0.0/255.0.0.0

# Paths For this example this machine needs to access 150.0.0.0/255.255.0.0 as
# well as port 80 on the network 150.1.0.0/255.255.0.0 through the socks 5
# server at 10.1.7.25 (if this machines hostname was "socks.hello.com" we could
# also specify that, unless --disable-hostnames was specified to ./configure).

path {
        reaches = 150.0.0.0/255.255.0.0 reaches = 150.1.0.0:80/255.255.0.0
        server = 10.1.7.25 server_type = 5 default_user = delius default_pass =
        hello
}

# Default server For connections that aren't to the local subnets or to
# 150.0.0.0/255.255.0.0 the server at 192.168.0.1 should be used (again,
# hostnames could be used too, see note above)

server = 127.0.0.1
# Server type defaults to 4 so we need to specify it as 5 for this one
server_type = 5
# The port defaults to 1080 but I've stated it here for clarity
server_port = 1080

#___________________________________________________________________________ END
#OF TEXT IS ONE LINE ABOVE



Tested on:
    ubuntu 12.04+ python 3.2+ tsocks 1.8


    
