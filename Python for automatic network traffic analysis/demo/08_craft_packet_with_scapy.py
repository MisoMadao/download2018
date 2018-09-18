from scapy.all import *

# How does scapy work to create a packet?

# a simple tcp packet
tcp_pkt = Ether()/IP()/TCP()
# print raw packet
print(tcp_pkt)
# show method is better ;)
print(tcp_pkt.show())

# a simple udp packet
udp_pkt = Ether()/IP()/UDP()
print(udp_pkt.show())

# set source and destination ips
src_ip = "10.1.1.1"
dst_ip = "8.8.8.8"
dst_port = 53
tcp_pkt[IP].src = src_ip
tcp_pkt[IP].dst = dst_ip
tcp_pkt[IP][TCP].dport = dst_port
tcp_pkt[IP].show()

# Let's add some content to our tcp packet
tcp_pkt[IP][TCP].payload = Raw("Hello world!")

# we can also create a pcap
wrpcap('single_pkt.pcap', tcp_pkt)

# how to send our packet? with the well known socket module
# (works only if you can reach host:port!)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((dst_ip, dst_port))
s.send(bytes(tcp_pkt))
print("packet sent!")
