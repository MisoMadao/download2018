import socket

# Packet capture with a raw socket
# This kind of socket captures all traffic, incoming and outgoing, for all protocols
#   To capture only some traffic you should do something like this:
#   s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#   this example captures only incoming tcp packets
#
# This sniffer shows you the raw data, you need to do some parsing for every header of the packet, very interesting
# work to do but also very strenuous
#
# reference: https://www.binarytides.com/python-packet-sniffer-code-linux/


def capture():
    try:
        print('start capture...')
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        while True:
            print(s.recvfrom(65565))

    except KeyboardInterrupt:
        print('\nfinish capture...')
        return


if __name__ == '__main__':
    capture()
