"""
    This program should not be executed directly. SSHTunnel.py should be executed instead to run the program.
"""


import subprocess
from SSHTunnelBaseClass import SSHTunnelBaseClass

class SSHDynamic(SSHTunnelBaseClass):
    """This base class defines the attributes necessary for SSH Tunnneling. It extends the base class which has general attributes for ssh connections.
        
        Some implementations ideas come from https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding
    """
    def __init__(self, user, server, key, password, port=1080):
        """ Constructor
            program: The command line argument to be executed. This is generally the program you want to launch with tsocks.
            port: The local port which will be dynamically fowarded to create the SSH tunnel. For now: THE PORT SHOULD BE LEFT AS 1080
                since we cannot modify /etc/tsocks.conf without sudo. Later on we can look into changing the location of this configuration file but that can be a security risk.
        """

        super().__init__(user, server, key)        
        """ Super constructor
        """
        self.password = password
        self.port = port
        
        
        
        
        
        
        
# GARBAGE AREA:
"""
tun1 = SSHDynamic("ubuntu",
                  "ec2-54-187-203-101.us-west-2.compute.amazonaws.com",
                  "/home/bluezone/amazon_ubuntu_key.pem",
                  "wine /home/bluezone/.wine/drive_c/ProgramFiles/DiabloII/DiabloII.exe -w")

"""



# super([type[, object-or-type]])
        #A type is anything that can be defined as a Class, and an object is
        #anything