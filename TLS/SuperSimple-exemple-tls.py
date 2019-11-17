# GPLv3 - github.com/theo546 (github.com/theo546/pyftpdlib-exemples)
# Dependencies: pyftpdlib, pyopenssl

from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

# Configuration
PORT = 2121
BIND = ''
CERTFILE_PATH = "cert.pem"
KEYFILE_PATH = "privkey.pem"

# FTP user directory
USER_DIRECTORY = "/opt/ftpserver/"

# This part has been copied and modified from the exemple here: https://pyftpdlib.readthedocs.io/en/latest/tutorial.html
if __name__ == "__main__":
	# Instantiate a dummy authorizer for managing 'virtual' users
	authorizer = DummyAuthorizer()

	# Define a new user having full r/w permissions and a user with read-only permissions.
	authorizer.add_user("test", "test", USER_DIRECTORY + "test", perm="elradfmwMT")
	authorizer.add_user("no_perm_user", "test2", USER_DIRECTORY + "no_perm_user", perm="elr")

	# Permissions are available here: https://pyftpdlib.readthedocs.io/en/latest/api.html#users

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