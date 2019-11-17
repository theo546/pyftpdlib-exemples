# GPLv3 - github.com/theo546 (github.com/theo546/pyftpdlib-exemples)
# Dependencies: pyftpdlib, pyopenssl

from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
import os

# Configuration
PORT = 2121
BIND = ''
CERTFILE_PATH = "cert.pem"
KEYFILE_PATH = "privkey.pem"
CREATE_FOLDER_IF_NOT_EXIST = True

# FTP user directory
USER_DIRECTORY = "/opt/ftpserver/"

# User list
USER_DATA = {
	"test": {
		"password": "test",
		"permissions": "elradfmwMT",
		"directory_override": "",
		"custom_directories_permissions": {
			"fuck": ""
		}
	},
	"override_test": {
		"password": "test2",
		"permissions": "elradfmwMT",
		"directory_override": "/opt/ftpserver/test",
		"custom_directories_permissions": {}
	},
	"no_perm_user": {
		"password": "test3",
		"permissions": "elr",
		"directory_override": "",
		"custom_directories_permissions": {
			"only_folder_i_can_access": "elradfmwMT",
			"only_folder_i_can_access/sub_folder_i_dont_have_permission": "elr"
		}
	}
}

# Permissions are available here: https://pyftpdlib.readthedocs.io/en/latest/api.html#users

class DummyAuthorizer(DummyAuthorizer):
	def __init__(self, user_data, user_directory, create_folder_if_not_exist):
		self.USER_DATA = user_data
		self.USER_DIRECTORY = user_directory
		self.CREATE_FOLDER_IF_NOT_EXIST = create_folder_if_not_exist
	
	def validate_authentication(self, username, password, handler):
		# Check if the provided username exist in the USER_DATA array, if not, fail the authentication.
		if username not in self.USER_DATA:
			print("User " + username + " doesn't exist")
			raise AuthenticationFailed
		# If the user exist, check if the provided password match with the one stored in the USER_DATA array, if not, fail the authentication.
		if self.USER_DATA[username]['password'] != password:
			print("Password for user " + username + " is invalid")
			raise AuthenticationFailed
		# If the variable CREATE_FOLDER_IF_NOT_EXIST has been set on True, create a folder for the user if it doesn't already exist.
		if self.CREATE_FOLDER_IF_NOT_EXIST:
			if not os.path.isdir(self.get_home_dir(username)):
				os.mkdir(self.get_home_dir(username))
	
	def get_home_dir(self, username):
		# Check if the user data have a directory override set, if yes, return it.
		if not self.USER_DATA[username]['directory_override']:
			return USER_DIRECTORY + username
		else:
			return self.USER_DATA[username]['directory_override']
	
	def has_perm(self, username, perm, path=None):
		print("Requested directory (" + username + "): " + path)

		exploded_path = path.split(self.get_home_dir(username) + "/")

		latest_valid_custom_permission = False

		# Does stuff...
		try:
			exploded_path = exploded_path[1].split("/")
		except:
			exploded_path = ['']
		for x in range(0, len(exploded_path)):
			if x == 0:
				check_path = exploded_path[0]
			else:
				check_path = ''
				for y in reversed(range(0, x + 1)):
					check_path = check_path + exploded_path[x - y] + "/"
				check_path = check_path[:-1]

			if check_path in self.USER_DATA[username]['custom_directories_permissions']:
				latest_valid_custom_permission = check_path

		# If the requested folder (or parent folder) has a valid custom permission, check if the user has the access to it.
		if latest_valid_custom_permission:
			if latest_valid_custom_permission in self.USER_DATA[username]['custom_directories_permissions']:
				if perm in self.USER_DATA[username]['custom_directories_permissions'][latest_valid_custom_permission]:
					return True

		# If no custom permission is set on the requested folder, just use return the user global permission.
		if perm in self.USER_DATA[username]['permissions']:
			return True
		
		# Return False if nothing was found.
		return False

	def get_perms(self, username):
		return self.USER_DATA[username]['permissions']
	
	def get_msg_login(self, username):
		return "Custom login message"

if __name__ == "__main__":
	# If the choosed user directory doesn't end with a slash, add one.
	if not USER_DIRECTORY.endswith('/'):
		USER_DIRECTORY = USER_DIRECTORY + "/"

	# If some folders in the user custom directories permissions array end with a slash, remove it.
	for KEY_USER, USER in USER_DATA.items():
		if USER['custom_directories_permissions']:
			for DIRECTORY in list(USER['custom_directories_permissions']):
				if DIRECTORY.endswith('/'):
					USER_DATA[KEY_USER]['custom_directories_permissions'][DIRECTORY[:-1]] = USER_DATA[KEY_USER]['custom_directories_permissions'].pop(DIRECTORY)

	# Instantiate a dummy authorizer for managing 'virtual' users
	authorizer = DummyAuthorizer(USER_DATA, USER_DIRECTORY, CREATE_FOLDER_IF_NOT_EXIST)

	# Instantiate FTP handler class
	handler = TLS_FTPHandler
	handler.authorizer = authorizer

	# Set TLS certificate and keyfile path
	handler.certfile = CERTFILE_PATH
	handler.keyfile = KEYFILE_PATH

	# Define a customized banner (string returned when client connects)
	handler.banner = "pyftpdlib based ftpd ready."

	# Specify a masquerade address and the range of ports to use for
	# passive connections.  Decomment in case you're behind a NAT.
	#handler.masquerade_address = '151.25.42.11'
	#handler.passive_ports = range(60000, 65535)

	# Instantiate FTP server class and listen on the choosed address and port above.
	server = FTPServer((BIND, PORT), handler)
	
	# Set a limit for connections, disabled here.
	#server.max_cons = 256
	#server.max_cons_per_ip = 5

	# Start FTP server
	server.serve_forever()