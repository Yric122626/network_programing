#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter02/udp_local.py
# UDP client and server on localhost

import argparse, socket
from datetime import datetime

##new
import socket
import struct
#from uuid import getnode as get_mac
from random import randint

MAX_BYTES = 65535
HOST_ADDR = '127.0.0.1'
server_port = 67 # DHCP server port
client_port = 8888 # DHCP client port

# client DISCOVER
def discover():
    #macb = getMacInBytes()
    macb = b''
    macb = b'\x00\x0C\x29\xD6\xBC\x5E' #host mac

    packet = b''
    packet += b'\x01'   #Message type: Boot Request (1)
    packet += b'\x01'   #Hardware type: Ethernet
    packet += b'\x06'   #Hardware address length: 6
    packet += b'\x00'   #Hops: 0 
    #packet += self.transactionID       #Transaction ID
    packet += b'\x39\x03\xF3\x26'

    packet += b'\x00\x00'    #Seconds elapsed: 0
    packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
    packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
    #packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
    packet += macb
    packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
    packet += b'\x00' * 67  #Server host name not given
    packet += b'\x00' * 125 #Boot file name not given
    packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
    packet += b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
    #packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
    packet += b'\x3D\x06' + macb
    packet += b'\x37\x03\x03\x01\x06'   #Option: (t=55,l=3) Parameter Request List
    packet += b'\xFF'   #End Option
    return packet

def request(offer_data):

    client_mac = b''
    client_mac += offer_data[28:34]

    magic_cookie = b''
    magic_cookie += offer_data[236:240]

    packet = b''
    packet += b'\x01'
    packet += b'\x01'
    packet += b'\x06'
    packet += b'\x00'
    packet += b'\x39\x03\xF3\x26'
    packet += b'\x00\x00'
    packet += b'\x00\x00' # Flag
    packet += b'\x00\x00\x00\x00' # client IP addr
    packet += b'\x00\x00\x00\x00' # your IP addr
    packet += b'\x00\x00\x00\x00' # server IP addr
    packet += b'\x00\x00\x00\x00' # gateway IP addr
    packet += client_mac
    packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
    packet += b'\x00' * 67  #Server host name not given
    packet += b'\x00' * 125 #Boot file name not given
    #packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
    packet += magic_cookie
    # option
    packet += b'\x35\x01\x03'
    packet += b'\x32\x04\xC0\xA8\x01\x60' # option 50 192.168.1.100 request
    packet += b'\x36\x04\xC0\xA8\x01\x01' # option 50 192.168.1.1 request
    packet += b'\xFF' # End option
    return packet

#Server
def offer(discover_data):
    
    client_mac =b''
    client_mac += discover_data[28:34]
    magic_cookie = b''
    magic_cookie += discover_data[236:240] 

    #print('Magic ID:',discover_data[236:240])
    packet = b''
    packet += b'\x02'
    packet += b'\x01'
    packet += b'\x06'
    packet += b'\x00'
    packet += b'\x39\x01\xF3\x26'
    packet += b'\x00\x00'
    packet += b'\x00\x00'
    packet += b'\x00\x00\x00\x00'
    packet += b'\xC0\xA8\x01\x64' #Your IP addr
    packet += b'\xC0\xA8\x01\x01' #Server IP addr
    packet += b'\x00\x00\x00\x00' #Gateway IP addr
    packet += client_mac
    packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
    packet += b'\x00' * 67  #Server host name not given
    packet += b'\x00' * 125 #Boot file name not given
    packet += magic_cookie   #packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
    
    # option
    packet += b'\x35\x01\x02'   #Option: (t=53,l=1) DHCP Message Type = DHCP OFFER
    packet += b'\x01\x04\xFF\xFF\xFF\x00' #netmask
    packet += b'\x36\x04\xC0\xA8\x01\x01' #DHCP server IP
    packet += b'\x33\x04\x00\x00\x0E\x10' #DHCF leastime
    packet += b'\xFF' #End Option
    return packet

def acknowledgement(data):
    client_mac =b''
    client_mac += data[28:34]

    magic_cookie = b''
    magic_cookie += data[236:240]
    
     #print('XID:',data[28:34])
    packet = b''
    packet += b'\x02'
    packet += b'\x01'
    packet += b'\x06'
    packet += b'\x00'
    packet += b'\x39\x01\xF3\x26'
    packet += b'\x00\x00'
    packet += b'\x00\x00'
    packet += b'\x00\x00\x00\x00' #client IP addr
    packet += b'\xC0\xA8\x01\x64' #Your IP addr
    packet += b'\xC0\xA8\x01\x01' #Server IP addr
    packet += b'\x00\x00\x00\x00' #Gateway IP addr
    packet += client_mac
    packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
    packet += b'\x00' * 67  #Server host name not given
    packet += b'\x00' * 125 #Boot file name not given
    #packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
    packet += magic_cookie

    #option
    packet += b'\x35\x01\x05'
    packet += b'\x01\x04\xFF\xFF\xFF\x00'
    packet += b'\xFF'
    return packet

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST_ADDR, server_port))
    print('Listening at {}'.format(sock.getsockname()))
    
    # receive DISCOVER part
    print('wait for DISCOVER packet...')
    while True:
        discover_data, address = sock.recvfrom(MAX_BYTES)
        if len(discover_data)>0:
            print('DISCOVER is received...')
            break
    
    # send OFFER part
    offer_text= offer(discover_data)
    sock.sendto(offer_text,(HOST_ADDR,client_port))
    print('dhcp offer has sent...')


    # receive REQUEST part
    print('wait for request packet...')
    while True:
    	request_data, address = sock.recvfrom(MAX_BYTES)
    	if len(request_data) > 0:
    		print('REQUEST is received...')
    		break

    # send ACKNOWLEDGEMENT
    ack_text = acknowledgement(request_data)
    sock.sendto(ack_text,(HOST_ADDR,client_port))
    print('Acknowledgement has sent...')
    print('Action Finish')

def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST_ADDR,client_port))

    # send DISCOVER part
    discover_text = discover()
    sock.sendto(discover_text,(HOST_ADDR,server_port))
    #sock.sendto(discover_text,(Broadcast_ADDR,server_port))
    print('dhcp discover has sent...')
    
    # receive OFFER part
    print('wait for Offer packet...')
    while True:
        offer_data, address = sock.recvfrom(MAX_BYTES)
        if len(offer_data)>0:
            print('offer_data receive...')
            break
    # send request part
    request_text = request(offer_data)
    sock.sendto(request_text,(HOST_ADDR,server_port))
    print('DHCP had sent request...')
    
    # receive ack part
    print('wait for Acknowledgement...')
    while True:
        ack_data, address = sock.recvfrom(MAX_BYTES)
        if len(ack_data)>0:
            print('Acknowledgement_data receive...')
            break
    print('Action Finish')

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    #parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        #help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    #function(args.p)
    function()
