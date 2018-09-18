from scapy.all import *


# As always doing things with scapy is much easier
# Notice how we build a full IP/uDP packet! One line!
# Run this script with an host as argument
#
# reference: https://jvns.ca/blog/2013/10/31/day-20-scapy-and-traceroute/

def traceroute(hostname):
    for i in range(1, 28):
        pkt = IP(dst=hostname, ttl=i)/UDP(dport=random.choice(range(33434, 33535)))

        reply = sr1(pkt, verbose=0, timeout=5)
        if reply is None:

            break
        elif reply.type == 3:

            print("Done!", reply.src)
            break
        else:

            print("%d hops away: " % i, reply.src)


if __name__ == '__main__':
    traceroute(sys.argv[1])
