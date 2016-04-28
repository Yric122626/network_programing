from struct import pack
from scapy.all import *
import argparse, socket
from datetime import datetime
# Initializing
conf.checkIPaddr = False
if __name__ == '__main__':
	packets = sniff(filter = 'port 67', timeout = 3)
	#packets.show()
	#print (packets[0][DHCP].options[0][1])
	if packets[0][DHCP].options[0][1]==1:
	# Build DHCP Offer Packet
		dhcp_off = Ether(src = "00:0c:29:4f:24:1c", dst = "00:21:9b:e3:ae:81")/IP(src = "127.0.0.1", dst = "127.0.0.1")/UDP(sport = 67, dport = 68)/BOOTP(chaddr = '1234567890abcdef')/DHCP(options = [("message-type", "offer")] )
		sendp(dhcp_off)
		packetss = sniff(filter = 'port 67', timeout = 12)
		#packetss.show()
		if packetss[0][DHCP].options[0][1]==3:
	# Build DHCP ACK Packet
			dhcp_ack = Ether(src = "00:0c:29:4f:24:1c", dst = "00:21:9b:e3:ae:81")/IP(src = "127.0.0.1", dst = "127.0.0.1")/UDP(sport = 67, dport = 68)/BOOTP(chaddr = '1234567890abcdef')/DHCP(options = [("message-type", "ack")] )			
			sendp(dhcp_ack)
		