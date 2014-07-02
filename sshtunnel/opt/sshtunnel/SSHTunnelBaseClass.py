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
