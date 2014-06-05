"""
    This program should not be executed directly. SSHTunnel.py should be executed instead to run the program.
"""

class SSHTunnelBaseClass:
	""" A super class which defines some attributes which are common to all SSH connections
	"""
	def __init__(self, user, server, key):
		""" A base class which defines some attributes which are common to all SSH connections
			user: The username used to login to the server (default is 'ubuntu' for amazon aws ubuntu instances)
			server: The remote server domain name (or ip)
			key: the identification key file (blank if no key file required)			
		"""		
		self.user = user
		self.server = server		
		self.key = key








# Pay no attention to this:

#Step 1:
#Start an ssh SOCKS bind to 1080 locally, 
#ssh -vvC -p22 -D1080 -i/home/bluezone/amazon_ubuntu_key.pem ubuntu@ec2-54-187-203-101.us-west-2.compute.amazonaws.com



#
"""
<Bashing-om> bluezone: It has been ages since I set up ssh, I am not the best person to ask. But ya ssh into your target machine, not to the router, the router will forward to port 22 on the machine.
<nith1210> bluezone: You are sshing from where to where?

<bluezone> nith1210, i suppose i am sshing to myself, i don't really understand. I'm trying to setup a dynamic port fowarding for SOCKS, one of the steps is something like this: ssh -vv -C -p9567  -D1080 bluezone-ubuntu

<bluezone> the port is fowarded on my router (9567) both externally and internally
* us`0gb (~0gb.us@c-71-237-219-28.hsd1.or.comcast.net) has joined #ubuntu
<bluezone> but the connection is refused
* troyready has quit (Remote host closed the connection)
* Guegs (~Guegs___@207-47-246-154.sktn.hsdb.sasknet.sk.ca) has joined #ubuntu
* Caveat (~kvirc@75-143-98-243.dhcp.aubn.al.charter.com) has joined #ubuntu
* CyberJacob is now known as CyberJacob|Away
* julieanna (~julieanna@64.124.192.210) has joined #ubuntu
<daftykins> bluezone: did you reconfigure sshd to run on that port and restart it afterward?
<nith1210> bluezone: Where is the machine that you're trying to ssh from?
<oneof3> hello. i installed ia-32libs by using the command sudo apt-get install ia-32libs. how can i remove it? sudo apt-get remove is-32libs wont work nor did sudo apt-get uninstall ia-32libs
* Thermo has quit (Quit: Textual IRC Client: www.textualapp.com)
<daftykins> Amy_Lu_Who: i have to sleep now, night \o
<Amy_Lu_Who> daftykins, thank you once again.  that was more about learning to install software than getting a silly old as heck game on here. :)  now it is time to go shopping...
* Zyrax (~zyrax@194.50.140.111) has joined #ubuntu
<daftykins> Amy_Lu_Who: buy me something nice!
* anthony__ has quit (Ping timeout: 250 seconds)
* lupfantomo has quit (Read error: Connection reset by peer)
<bluezone> daftykins, i'm not sure what you mean, so probably no :( I'm not an expert in this field,  nith1210 i am sshing from my own machine right next to me and basically that is also bluezone-ubuntu
<Amy_Lu_Who> hehe.  i was thingk photoshpop pro, i have the hubby's cretit card...
<bluezone> nith1210, i.e. the full command with the user is: bluezone@bluezone-ubuntu:~$ ssh -vv -C -p9567  -D1080 bluezone-ubuntu
* maximski (~maximski@77-20-48-40-dynip.superkabel.de) has joined #ubuntu
* maximski has quit (Max SendQ exceeded)
* delinquentme (~dingo@74.61.157.78) has joined #ubuntu
* AndresSM_ has quit (Quit: Leaving)
* enmand (~mb@sydnns0109w-142068200108.dhcp-dynamic.FibreOp.ns.bellaliant.net) has joined #ubuntu
<bluezone> i was told to do this here: https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding  Under 'dynamic port fowarding'
* maximski (~maximski@77-20-48-40-dynip.superkabel.de) has joined #ubuntu
* AndresSM_ (~Andres@186.4.143.107) has joined #ubuntu
* jsamuel has quit ()
* xangua (~angel@unaffiliated/xangua) has joined #ubuntu
<nith1210> bluezone: the command isn't wrong, you're having a connection issue.
<daftykins> Amy_Lu_Who: i wouldn't recommend buying windows programs and expecting them to run on ubuntu without first looking at the WINE compatibility database - but even then it's best to try out free native programs instead, check out 'The GIMP' for an image editing program
* oneof3 has quit (Client Quit)
* ryan_46 has quit (Ping timeout: 276 seconds)
<daftykins> anyway ta-ra \o
<nith1210> bluezone: but you're trying to ssh into yourself with that command
* ziyourenxiang (~ziyourenx@unaffiliated/ziyourenxiang) has joined #ubuntu
* enmand has quit (Client Quit)
<nith1210> bluezone: I'd bet if you do "ssh -vv -C -p22 -D1080 bluezone-ubuntu" it might work.
<bluezone> nith1210, so does that even require any port fowarding at all?
<bluezone> hmm ok
* dayangkun_ (~dayangkun@101.78.195.61) has joined #ubuntu
<nith1210> bluezone: no, the dynamic port forward doesn't make sense through the machine you're already on.
* julieanna has quit (Ping timeout: 258 seconds)
<bluezone> nope, ssh: connect to host bluezone-ubuntu port 22: Connection refused
<nith1210> bluezone: what port is sshd running on?
* Toph (~peace@h69-31-230-220.dynamic.platinum.ca) has joined #ubuntu
<Amy_Lu_Who> daftykins, will do.  i am still getting used to the transition.  i have seen the light.  thank you again and good night.
* lazarus_ (~liam@cpc9-gate10-2-0-cust5.16-2.cable.virginm.net) has joined #ubuntu
* willyg_cos has quit (Quit: Leaving)
* code_zombie has quit (Quit: Leaving)
* wafflejock_ (~quassel@c-98-213-47-190.hsd1.il.comcast.net) has joined #ubuntu
* UbuntuBoy (~rickpeezy@73.51.110.220) has joined #ubuntu
* wisewise has quit (Ping timeout: 258 seconds)
<bluezone> nith1210, not installed
<bluezone> i guess that's the problem
* baustin (~baustin@rrcs-71-42-213-98.sw.biz.rr.com) has joined #ubuntu
* m0e42 has quit (Ping timeout: 276 seconds)
<bluezone> the docs don't even mention anything about this though...
<nith1210> bluezone: what's the over-arching thing you're trying to do?
* mEck0 has quit (Quit: mEck0)
* Bucky21659 (~Player@ip24-250-76-36.br.br.cox.net) has joined #ubuntu
* anthony__ (~anthony@199.231.242.170) has joined #ubuntu
* dayangkun has quit (Ping timeout: 258 seconds)
* Tin_man has quit (Quit: Leaving)
* timh (~pete@192-0-154-83.cpe.teksavvy.com) has joined #ubuntu
* bocaneri (~bocaneri_@about/linux/staff/sauvin) has joined #ubuntu
* matnel (~matnel@humanisti.fixme.fi) has joined #ubuntu
<bluezone> nith1210, i'm trying to basically use tsocks for some applications to have them use my amazon aws console instead of my own network (directly)
* sysroot has quit (Remote host closed the connection)
<bluezone> (not the console but my amazon instance :P)
<timh> anyone expert at nvidia driver installs?    I have a boot up of constant 'nouveau' lines - what happened?  I don't even know what to google :-(
* aterdeus (~superior@176.43.194.162) has joined #ubuntu
* Brumble (~Brumble@66.117.111.244) has joined #ubuntu
* Tonee has quit (Read error: Connection reset by peer)
* Aki-XchatCrashed (~Aki-Think@135.0.189.14) has joined #ubuntu
* __raven (~raven@dslb-092-074-210-148.pools.arcor-ip.net) has joined #ubuntu
<lazarus_> how do i boot an iso direct frm HDD using grub 2
* io_____ has quit (Quit: Connection closed for inactivity)
<Yelu> bluezone, each machine you want to ssh in, must have a running sshd (sudo apt-get install openssh-server) listening to incoming connections
* UbuntuBoy has quit (Client Quit)
<timh> I replaced an old nvidia card with a new one... I think I know how to fix the issue but I cannot even get to a terminal shell because 'nouveau' text scrolls down forever
<Brumble> Hi guys, If any ones able I need some help figuring something out on ubuntu :)
<timh> hi
<Brumble> Hi :)
<Beldar> lazarus_, https://help.ubuntu.com/community/Grub2/ISOBoot
<nith1210> bluezone: are you able to ssh into your aws machine?
<timh> lazarus_: you want to use a live media like from a usb flash drive?
<bluezone> Yelu, thanks for the explanation, i was just about to type that in question form hehe. Perhaps they should add this in the docs though! https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding
<bluezone> nith1210, yes
<Brumble> in ubuntu 14 is it normal to have a fat32 partition /boot/efi?
* troyready (~troyready@199.19.145.16) has joined #ubuntu
<nith1210> bluezone: what port is it on?
<bluezone> i believe it is on port 22
* Player has quit (Ping timeout: 276 seconds)
<Yelu> bluezone, and check your firewall for the ports you're using (22 or what you defined there)
* Destine (~Destine@ubuntu/member/Destine) has joined #ubuntu
* pauxlo (~pauxlo@137.119.162.151) has joined #ubuntu
* Exancillatus (~Exancilla@127-29-190-109.dsl.ovh.fr) has joined #ubuntu
<Bashing-om> lazarus_: See: -> https://help.ubuntu.com/community/Grub2/ISOBoot  .
<Yelu> bluezone, sudo netstat -tulp
* sxp2 (~sxp@181.29.89.234) has joined #ubuntu
* lucastt_ has quit (Quit: Saindo)
* pauxlo is now known as lupfantomo
* sudormrf has quit (Read error: Connection reset by peer)
<Yelu> bluezone, that will give you the running services
* ADW (ADW@host-69-145-5-59.chy-wy.client.bresnan.net) has joined #ubuntu
* king1337-2 has quit (Quit: Leaving)
* jondavis (~jondavis@99-43-76-50.lightspeed.hstntx.sbcglobal.net) has joined #ubuntu
* baustin has quit (Ping timeout: 258 seconds)
* barium_bitmap has quit (Ping timeout: 250 seconds)
* Pencil_ (~joe@71.196.202.3) has joined #ubuntu
* kkkkkkkkk (~kkkkkkkkk@179.186.93.15.dynamic.adsl.gvt.net.br) has joined #ubuntu
* jondavis has quit (Client Quit)
* professor_soap has quit ()
<nith1210> bluezone: in the ssh command you want, you want to use ssh -vvC -p<port1> -D<port2> <host>
* agis has quit (Ping timeout: 258 seconds)
* anthony__ has quit (Ping timeout: 276 seconds)
<nith1210> bluezone: <port1> is the port ssh is on. <port2> is the local port. <host> is the machine you want to push packets through
<Bashing-om> Brumble: Ya got Windows * and/or GPT partitioning, then yep you will see a /boot/efi partition.
<nith1210> bluezone: the local port has to be free and unused, 1080 is a good number for this.
<Pencil_> hello
* pmciano_ has quit (Quit: My MacBook has gone to sleep. ZZZzzz…)
* ryan_46 (~yance@68-113-41-147.static.mdfd.or.charter.com) has joined #ubuntu
<Brumble> Well I don't have windows thats why it concerns me lol
<bluezone> nith1210, this is like the local port fowarding section right?
* phuh (~phuh@cp66-203-194-42.cp.telus.net) has joined #ubuntu
<Bashing-om> Brumble: Then I recon ya got a disk that is partitioned in the GPT format.
* sxp has quit (Ping timeout: 252 seconds)
<bluezone> nith1210, is it the same as this? ssh -L 8080:www.ubuntuforums.org:80 <host>
* AndresSM_ has quit (Ping timeout: 255 seconds)
<nith1210> bluezone: it's not the same as that, but similar
<bluezone> hmm
<Brumble> Thanks for the help :)
* jason_ has quit (Ping timeout: 252 seconds)
<nith1210> bluezone: put it like this
* Exancillatus has quit (Ping timeout: 258 seconds)
"""
