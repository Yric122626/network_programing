from struct import pack
from scapy.all import *
import argparse, socket
from datetime import datetime
# Initializing
conf.checkIPaddr = False

#def client(port):
if __name__ == '__main__':
	# Build DHCP Discovery Packet
	dhcp_disc = Ether(src = "00:0c:29:4f:24:1c", dst = "00:0c:29:4f:24:1c")/IP(src = "127.0.0.1", dst = "127.0.0.1")/UDP(sport = 68, dport = 67)/BOOTP(chaddr = '1234567890abcdef')/DHCP(options = [("message-type", "discover"), "end"])
	sendp(dhcp_disc)
	packet = sniff(filter = 'port 68 ', timeout = 5)
	#packet[0][DHCP].show()
	#print(packet[0][DHCP].options[0][1])
	#if len(packet[0])>1:
	if packet[0][DHCP].options[0][1] == 2 :
	# Build DHCP Request Packet
		dhcp_request = Ether(src = "00:0c:29:4f:24:1c", dst = "00:0c:29:4f:24:1c")/IP(src = "127.0.0.1", dst = "127.0.0.1")/UDP(sport = 68, dport = 67)/BOOTP(chaddr = '1234567890abcdef')/DHCP(options = [("message-type", "request")])
		sendp(dhcp_request)