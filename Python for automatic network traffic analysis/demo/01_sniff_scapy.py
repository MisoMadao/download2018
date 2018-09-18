from scapy.all import *

# Packet capture with scapy
# This tool does most of the job for us, captures traffic and parses it, every packet is an object which is sent to a
# function to show it.
#   You can add some options to the sniffer, such as the interface or filters on the capture.
#   The pkt.show() function shows us the packet parsed with all the headers, we can substitute that with something
#   more adapt to our needs.


def pkt_callback(pkt):
    pkt.show()


def capture():
    try:
        print('start capture...')
        sniff(prn=pkt_callback, store=0)
    except KeyboardInterrupt:
        print('finish capture...')
        return


if __name__ == '__main__':
    capture()
