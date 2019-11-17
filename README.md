# pyftpdlib-exemples
A repo I made with some exemples (and even a fully working FTP system) for pyftpdlib.

## How to install?
Open a terminal then create a virtualenv using `python3 -m venv env`.

Then activate the virtualenv using `source env/bin/activate`.

Make sure that the wheel Python package is installed: `pip install wheel`.

Install the dependencies with `pip install pyftpdlib pyopenssl`.

Make sure that you have generated the "cert.pem" and "privkey.pem" files before starting a TLS server version.

You can generate those files with this command: `openssl req -newkey rsa:4096 -nodes -sha512 -x509 -days 365 -nodes -out cert.pem -keyout privkey.pem`

Then finally, run with `python *version you choosed*`.

If you didn't touched the configuration of the server, you should be able to connect to the server using this address: 127.0.0.1:2121.