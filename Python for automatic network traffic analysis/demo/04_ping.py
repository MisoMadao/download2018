from pythonping import ping
import sys

# Ping in python, very simple, isn't it?
# But try to take a look at the underlying code here: https://github.com/alessandromaggio/pythonping
# This module uses the already seen socket module
#
# run the script with an ip address or a domain name as argument

if __name__ == '__main__':
    ping(sys.argv[1], verbose=True)
