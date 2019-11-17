# pyftpdlib-exemples
A repo I made with some exemples (and even a fully working FTP system) for pyftpdlib.

## How to install?
Open a terminal then create a virtualenv using `python3 -m venv env`.

Then activate the virtualenv using `source env/bin/activate`.

Install the dependencies with `pip install pyftpdlib pyopenssl`.

Make sure that you have generated the "cert.pem" and "privkey.pem" file before starting a TLS server version.

Then finally, run with `python *version you choosed*`.

If you didn't touched the configuration of the server, you should be able to connect to the server using this address: 127.0.0.1:2121.