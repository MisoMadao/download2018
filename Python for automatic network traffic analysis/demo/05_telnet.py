from telnetlib import Telnet
import sys
import socket

# telnetlib is a very useful python module
# But try to take a look at the underlying code here: https://github.com/alessandromaggio/pythonping
# This module uses the already seen socket module
#
# Here is implemented a dumb telnet client

if __name__ == '__main__':
    hostname = sys.argv[1]
    port = sys.argv[2]
    print('Trying {}...'.format(socket.gethostbyname(hostname)))
    t = Telnet(hostname, port)
    print('Connected to {}.'.format(hostname))
    t.interact()
