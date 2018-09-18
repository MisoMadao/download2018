import socket
import sys

# A simplified nslookup with a raw socket
# This script does a name server lookup with the info retrieved by the socket
# Run this script with a domain as argument
#
# For reference about the socket.getaddrinfo method
# https://docs.python.org/3/library/socket.html#socket.getaddrinfo
#
# You can expand this by adding more options, you can use the argparse module to help you with this
# Sure to implement a complete nslookup you have to script a lot
#
# reference: https://stackoverflow.com/questions/12297500/python-module-for-nslookup


def nslookup(element):
    ip_list = []
    ais = socket.getaddrinfo(element, 0)
    for result in ais:
        ip_list.append(result[-1][0])
    ip_list = list(set(ip_list))
    for _ in ip_list:
        print('{}\tName: {}'.format(_, socket.getfqdn(_)))


if __name__ == '__main__':
    nslookup(sys.argv[1])
