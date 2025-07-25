#!/usr/bin/python3

#import PySide classes
import sys

import os

from threading import Thread
import time
from time import sleep

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import QWebView

from SSHDynamic import SSHDynamic

import shutil #to remove an entire directory tree (i.e. any non empty folder)
import subprocess
from subprocess import CalledProcessError
from subprocess import Popen
from subprocess import check_call
from subprocess import PIPE

import getpass # To get the username

import shlex #From python3.4

import traceback
import webbrowser

global LOGNAME
LOGNAME = getpass.getuser()


class StartingWindow(QDialog):
    """The starting window propmt
    """
    def __init__(self, parent= None):
        super(StartingWindow, self).__init__(parent)
        if LOGNAME == 'root':
            print("DO NOT RUN THE APPLICATION AS ROOT")
            sys.exit(0)
        
        #set_tsocks_conf_envvar()
        #Modify the tsocks configuration file in home dir.
        #modify_tsocks_conf()
        
        # Create a Label and show it
        self.label = QLabel("<em>Hide your identity online</em>")
        
        self.bExistingProxy = QPushButton("I Have a Server or VPS") #Button
        self.bSetUpProxy = QPushButton("I Need to Buy a VPS")
        
        #### Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.bExistingProxy)
        layout.addWidget(self.bSetUpProxy)
        self.setLayout(layout)
        ####
        #On click event        
        self.bExistingProxy.clicked.connect(self.show_server_form)
        self.bSetUpProxy.clicked.connect(self.show_ads)
        
        self.setWindowTitle("SSHTunneling")
        #self.ssh_credentials_dialog = None 
    def show_server_form(self):
        #starting_window.hide()
        self.ssh_credentials_dialog = SSHCredentialsDialog()            
        self.ssh_credentials_dialog.show()
    def show_ads(self):
        webbrowser.open_new_tab("http://zerorooter.bplaced.net/ads.html")
        
class Ads(QWebView):
    """DEPRECATED (NO LONGER BEING USED)
    Webview containing Advertisements (affiliate) to purchase vps servers.
    """
    def __init__(self, parent=None):
        LOGNAME = getpass.getuser() # LINUX DEPENDANT, LOGNAME is the current user
        super(Ads, self).__init__(parent)
        self.setWindowTitle("SSHTunneling: Purchase a server")
     
        ###
        layout = QVBoxLayout()
        
        ###
        self.setLayout(layout)
        
class SSHCredentialsDialog(QDialog):
    """A dialog that the user must fill out. It contains the username, keyfile location, server hostname, etc.
    """
    def __init__(self, parent=None):
        LOGNAME = getpass.getuser() # LINUX DEPENDANT, LOGNAME is the current user
        super(SSHCredentialsDialog, self).__init__(parent)
        self.setWindowTitle("SSHTunneling: Server setup and connect")
        #Attributes for setting up the SOCKS proxy
        self.user_prompt = QLabel("Username used to connect to server: ")
        self.user = QLineEdit("")
        self.server_prompt = QLabel("Server IP:")
        self.server = QLineEdit("")
        self.key_prompt = QLabel("ABSOLUTE path of the key file, blank if using password authentication")
        self.key = QLineEdit("")  
        self.sumbit = QPushButton("Submit and Connect")#Fowards the port 1080 locally and turns the ssh client into a SOCKS Proxy
        self.password_prompt = QLabel("Password: (blank if using key file authentication)")
        self.password = QLineEdit("")
        self.password.setEchoMode(QLineEdit.Password)
        
        #Create folder sshtunnel if it doesn't already exist
        os.chdir("/home/" + LOGNAME + "/.cache/")
        list_of_files = os.listdir()
        if "sshtunnel" not in list_of_files:
            subprocess.call(['mkdir', 'sshtunnel'])
       
        
        ##Retreive previously entered info
        os.chdir("/home/" + LOGNAME + "/.cache/sshtunnel/")
        list_of_files = os.listdir()
        if "SSHTunnelCredentials" not in list_of_files:
            #Create the file if it doesn't exist yet
            subprocess.call(['touch', 'SSHTunnelCredentials'])
        
        
        credentials = open("SSHTunnelCredentials", "r")
        self.user = QLineEdit(credentials.readline()[0:-1])#Cut off the \n at then end
        self.server = QLineEdit(credentials.readline()[0:-1])#Cut off the \n at then end
        self.key = QLineEdit(credentials.readline()[0:-1])#Cut off the \n at then end
        credentials.close()
        ##
        
        
        #
        self.key.setFixedWidth = 500
        ###
        layout = QVBoxLayout()
        layout.addWidget(self.user_prompt)
        layout.addWidget(self.user)
        layout.addWidget(self.server_prompt)
        layout.addWidget(self.server)
        layout.addWidget(self.key_prompt)
        layout.addWidget(self.key)
        
        layout.addWidget(self.sumbit)
        
        
        ###
        self.setLayout(layout)
        
        
        self.sumbit.clicked.connect(self.connect)
        
        self.sshtun = None #Done to keep sshtun alive
        self.errmsg = None #Done to keep errmsg alive
    def connect(self, local_port="1080"):
        """Establish an ssh connection
        Coverts the ssh client into a SOCKS proxy via Dynamic port fowarding
        """
        try:           
            self.sshtun = SSHDynamic(self.user.text(), self.server.text(), self.key.text(), "NOT IMPLEMENTED")
            LOGNAME = getpass.getuser() # LINUX DEPENDANT, LOGNAME is the current user    
            
            save_ssh_credentials(self.user.text(),self.server.text(), self.key.text())      
            
                           
            Popen(['fuser', '-k', '1080/tcp']) # Kills all tcp on 1080
            os.system('clear')
            
            print ("\nPAY ATTENTION TO THE TERMINAL, YOU MAY HAVE TO ENTER YOU'RE PASSWORD IF YOU ARE NOT USING A KEY-FILE\nIf nothing happens try to reconnect with the 'I Have a Server or VPS' button\n\n")
            
            if self.sshtun.key is not '': 
                pobj = Popen(['ssh','-Ctt','-o', 'GSSAPIAuthentication=no','-o', 'StrictHostKeyChecking=no', '-D'+local_port,'-i',str(self.sshtun.key),str(self.sshtun.user) +'@' +str(self.sshtun.server)])
                """
                c_time = time.time()
                while (time.time() != (c_time+4)): # pause for 4 seconds
                    pass
                """
                if pobj.poll() == None:
                    #Process hasn't terminated yet, so we are probably connected
                    starting_window.ssh_credentials_dialog.hide() #Hide the server form window
                    starting_window.launchApp_window = LaunchApp()
                    starting_window.launchApp_window.show()
                else:
                    #Process terminated so conection failed
                    print("CONNECTION FAILED")
                    
            elif self.sshtun.key == '':
                pobj = Popen(['ssh -Ctt -o GSSAPIAuthentication=no -o StrictHostKeyChecking=no -D' +local_port + " " + shlex.quote(self.sshtun.user)+'@'+str(self.sshtun.server)], shell=True)
                """
                c_time = time.time()
                while (time.time() < (c_time+4)): # pause for 4 seconds, regular sleep() wasn't fucking sleeping
                    pass
                    """
                if pobj.poll() == None:
                    #Process hasn't terminated yet, so we are probably connected
                    starting_window.ssh_credentials_dialog.hide() #Hide the server form window
                    starting_window.launchApp_window = LaunchApp()
                    starting_window.launchApp_window.show()
                else:
                    #Process terminated so conection failed
                    print("CONNECTION FAILED")
            #At this point, the process has exited, so we cannot possibly be connected
            """
            Not supported on python3.2
            except subprocess.TimeoutExpired:
                #At this point the process has not exited after 3.5 seconds, either the connection is taking long or
                #we are connected
                
                starting_window.ssh_credentials_dialog.hide() #Hide the server form window
                starting_window.launchApp_window = LaunchApp()
                starting_window.launchApp_window.show()
            """  
        
        except CalledProcessError as e:
            print(e)
            self.errmsg = ErrorMessage(str(e))
            self.errmsg.show()        
        
class LaunchApp(QDialog):
    """Pop-up dialog Window which allows you to tunnel firefox, chrome, and almost any other application through your SHH Tunnel
    WARNING: We are having problems with certain console based applications that are launched with tsocks, the programs sometimes fail to connect properly
    """
    def __init__(self, parent=None):
        super(LaunchApp, self).__init__(parent)
        self.setWindowTitle("SSHTunneling: Protect Internet browsing or some other application")
        #Attributes for setting up the SOCKS proxy
        
        self.sshtun = starting_window.ssh_credentials_dialog.sshtun
        
        self.info_browse = QLabel("""
                           <b>SOCKS proxy:</b> routed locally (<em>ip: 127.0.0.1</em>) on the port: <em>1080</em> <br/>
                            Enter the above information in your browser's PROXY settings or click one of the buttons below<br/>
                            <br/>
                            <b><em>WARNING: </em>This might close any firefox/chrome windows you have opened! You can re-open your session later</b><br/>""")
        
        self.firefox = QPushButton("Launch special Firefox instance")
        self.chrome = QPushButton("Launch special Chrome instance")
        
        self.info_other = QLabel("Traffic other applications by writing the path to the program below (followed by any arguments needed):") 
        self.program = QLineEdit("Program to launch")
        self.launch = QPushButton("Launch!")
        
        
        
        ###
        layout1 = QVBoxLayout()
        layout1.addWidget(self.info_browse)
        
        layout2 = QHBoxLayout()
        layout1.addLayout(layout2)
        layout2.addWidget(self.firefox)
        layout2.addWidget(self.chrome)
        
        layout1.addWidget(self.info_other)
        layout1.addWidget(self.program)
        layout1.addWidget(self.launch) 
        ###
        self.setLayout(layout1)
        
        self.firefox.clicked.connect(self.launch_firefox)
        self.chrome.clicked.connect(self.launch_chrome_instance)
        self.launch.clicked.connect(self.launch_program)
    def launch_program(self):
        """Tunnel programs which do not have SOCKS proxy settings, uses tsocks.
        """
        args = self.program.text()
        args = shlex.quote(args)
        
        #gnome-terminal or xterm must be installed otherwise console-based applications may not work
        ap_gt = subprocess.Popen("apt-cache policy gnome-terminal", shell = True, universal_newlines = True, stdout=PIPE)
        ap_gtstdout, stderr = ap_gt.communicate()
        
        ap_xt = subprocess.Popen("apt-cache policy xterm", shell = True, universal_newlines = True, stdout=PIPE)
        ap_xtstdout, stderr = ap_xt.communicate()
        
        if "(none)" not in ap_gtstdout:
            #gnome-terminal is installed
            subprocess.Popen("gnome-terminal -x tsocks " + args, shell=True, universal_newlines = True)
        elif "(none)" not in ap_xtstdout:
            #xterm is installed
            subprocess.Popen("xterm -e tsocks " + args, shell=True, universal_newlines = True)
        else:
            #Run it in same terminal
            subprocess.Popen("tsocks " + args, shell=True, universal_newlines = True)
        
    def launch_chrome_instance(self):
        """Kill all chrome instances and launch a new instance with
        --proxy-server=socks5://127.0.0.1:1080
        
        Chrome instances seem to need to be killed before we can launch a special instance
            otherwise the new instance will not tunnel through SSH at all."""
        
        subprocess.call(["killall", "chrome"]) #all chrome instance must be killed
        sleep(1)
        subprocess.Popen(["google-chrome","--proxy-server=socks5://127.0.0.1:1080", "--no-default-browser-check"])
        
    def launch_firefox(self, host = "127.0.0.1", port=1080):
        """Launches the special firefox instance under the 'SSHTunnel' profile. Also,
            modifies the proxy settings inside the 'SSHTunnel' firefox profile (creates the profile if necessary)
        """
        
        #If
        #@deprecated
        self.LOGNAME = LOGNAME # LINUX DEPENDANT, LOGNAME is the current user (global variable defined at the top)
        
        #Success: created profile 'random' at '/home/bluezone/.mozilla/firefox/jn6osaqs.random/prefs.js'
        os.chdir('/home/'+ str(self.LOGNAME) +'/.mozilla/firefox/')
        list_of_items = os.listdir(os.getcwd())
        
        profile_folder_name = None
        for folder in list_of_items:
            if 'SSHTunnel' in folder:
                profile_folder_name = folder
                
                os.chdir(folder)
                list_of_items = os.listdir(os.getcwd())
                for file_name in list_of_items:
                    if 'prefs.js' in file_name:
                        prefs = open('prefs.js')
                        prefs_text = prefs.read()
                        if ("network.proxy.socks" not in prefs_text or "network.proxy.no_proxies_on" not in prefs_text or
                            "network.proxy.type" not in prefs_text or "network.proxy.socks_port" not in prefs_text or
                            "network.proxy.socks_remote_dns" not in prefs_text):
                            #We need to create the profile again
                            print("re-Creating profile SSHTunnel")
                            os.chdir('/home/'+ str(LOGNAME) +'/.mozilla/firefox/')
                            shutil.rmtree(profile_folder_name);
                            self.create_profile_F()
                        else:
                            self.launch_firefox_instance()
                        break
                    
        else:
            if profile_folder_name == None:                
                self.create_profile_F()
        
        
       
    def create_profile_F(self):
        """Function to create the SSHTunnel Firefox profile
        All firefox instances must be closed
        (or they can be left open, but the function will killall firefox)        
        """
       
        
        subprocess.call(["killall", "firefox"]) #all firefox instance must be killed
        subprocess.check_call(["firefox","-CreateProfile","SSHTunnel"]) #Create a new Profile named SSHTunnel
      
        
        #Navigate to the profile folder:
        os.chdir('/home/'+ str(LOGNAME) +'/.mozilla/firefox/')
        list_of_items = os.listdir(os.getcwd())
        for folder in list_of_items:
            if 'SSHTunnel' in folder:
                os.chdir(folder)
                break
        else:
            raise Exception("Create new profile for firefox failed")
                        
        
        write_prefs_js()       
        
        self.launch_firefox_instance()
   
   
    def launch_firefox_instance(self, port= "1080"):
        """Launches an isolated firefox instance under the profile SSHTunnel and routes the traffic through the SOCKS proxy
            The settings are rewritten just incase something went wrong
        """
        #Navigate to the profile folder:
        os.chdir('/home/'+ str(LOGNAME) +'/.mozilla/firefox/')
        list_of_items = os.listdir(os.getcwd())
        for folder in list_of_items:
            if 'SSHTunnel' in folder:
                os.chdir(folder)
                break
        
        write_prefs_js()
        
        subprocess.Popen(["firefox","-no-remote", "-P", "SSHTunnel"]) #-no-remote allows you to have multiple profiles opened at the same time

class ErrorMessage(QDialog):
    """This Class defines a QDialog pop-up style error message, I Don't believe it is being used at the moment.
    """
    def __init__(self, title='Error', message='Something went wrong, please modify settings and try again'):
        super(ErrorMessage, self).__init__()
        self.title = title
        self.setWindowTitle(self.title)
        self.message = message
        
        self.errmessage = QLabel(self.message)
        self.ok = QPushButton("Ok")
         
        ###
        layout = QVBoxLayout()
        layout.addWidget(self.errmessage)
        layout.addWidget(self.ok)        
        ###
        
        self.setLayout(layout)
        self.ok.clicked.connect(self.close_window)
        
        
    def close_window(self):
        self.hide()
        


def write_prefs_js():
    """Writes the necessary settings in the preferences file for the firefox profile named 'SSHTunnel'.
    """
    ##Navigate to the profile folder
    os.chdir('/home/'+ str(LOGNAME) +'/.mozilla/firefox/')
    list_of_items = os.listdir(os.getcwd())
    for folder in list_of_items:
        if 'SSHTunnel' in folder:
            os.chdir(folder)
            break
    ##
    
    #Remove all the contents in prefs_temp.js
    prefs_temp = open("prefs_temp.js", "w")
    prefs_temp.write('')
    prefs_temp.close()
    
    #Modify the profile settings. This will force the firefox instance to connect to the SOCKS proxy 127.0.0.1:1080 (created by openSSH via Dynamic Port Fowarding in the connect() function)
    prefs_temp = open("prefs_temp.js", "w") #Open a temporary file for writing
    prefs = open("prefs.js", "r") #Open the preferences file for reading
    
    line = prefs.readline()
    ##Create a copy of prefs.js, without copying the preferences involving proxies.
    while (line != ''):        
        if "network.proxy." not in line:            
            prefs_temp.write(line)
        line = prefs.readline()
    prefs.close()
    prefs_temp.close()
    
    #Append the proxy settings in prefs_temp.js
    prefs_temp = open("prefs_temp.js", "a")    
    with open("prefs.js") as p:    
        prefs_temp.write('user_pref("network.proxy.socks", "127.0.0.1");\n')
        prefs_temp.write('user_pref("network.proxy.no_proxies_on", "");\n')
        prefs_temp.write('user_pref("network.proxy.type", 1);\n')
        prefs_temp.write('user_pref("network.proxy.socks_port", 1080);\n')
        prefs_temp.write('user_pref("network.proxy.socks_remote_dns", true);\n')   # IMPORTANT: protects against DNS leaks!       
    prefs_temp.close()
    ##
    
    #Copy over the prefs_temp.js file into the original prefs.js file
    prefs = open("prefs.js", "w") #Open for writing
    prefs_temp = open("prefs_temp.js", "r") #Open for reading    
    line = prefs_temp.readline()
    while (line != ''):
        prefs.write(line)
        line = prefs_temp.readline()
        
    prefs.close()
    prefs_temp.close()
    

def save_ssh_credentials(user,server,key):
    """Save the ssh credentials from the SSHCredentialsDialog so that we can retrieve them later
    Does not save the password since this is in plain text
    """
     #Create folder sshtunnel if it doesn't already exist
    os.chdir("/home/" + LOGNAME + "/.cache/")
    list_of_files = os.listdir()
    if "sshtunnel" not in list_of_files:
        subprocess.call(['mkdir', 'sshtunnel'])
    
    
    
    os.chdir("/home/" + LOGNAME + "/.cache/sshtunnel/")
    list_of_files = os.listdir()
    if "SSHTunnelCredentials" not in list_of_files:
        #Create the file if it doesn't exist yet
        subprocess.call(['touch', 'SSHTunnelCredentials'])
    
    credentials = open("SSHTunnelCredentials", "w")
    credentials.write(user+"\n")
    credentials.write(server+"\n")
    credentials.write(key+"\n")
    credentials.close()
    
    
def set_tsocks_conf_envvar():
    """Sets the configuration file envorionment variable for this terminal session """
    os.environ["TSOCKS_CONF_FILE"] = "/home/"+LOGNAME+"/tsocks.conf"

def modify_tsocks_conf():
    tsocks_text = """# This is the configuration for libtsocks (transparent socks)
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

# Default server
# For connections that aren't to the local subnets or to 150.0.0.0/255.255.0.0
# the server at 192.168.0.1 should be used (again, hostnames could be used
# too, see note above)

server = 127.0.0.1
# Server type defaults to 4 so we need to specify it as 5 for this one
server_type = 5
# The port defaults to 1080 but I've stated it here for clarity 
server_port = 1080"""
    
    config = open("/home/"+LOGNAME+"/tsocks.conf",'w')


    config.write(tsocks_text)
    config.close()








# Start the application:
app = QApplication(sys.argv)
starting_window = StartingWindow()
starting_window.show()

# Enter Qt application main loop
app.exec_()

sys.exit()

