#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import threading
import numpy
import time
import sys
import socket
import xmlrpclib
import binascii
from gnuradio import gr

class HummingbirdToXMLRPC(gr.sync_block):
    """
    docstring for block HummingbirdToXMLRPC
    """
    def __init__(self, xmlrpcAddr, xmlrpcPort, hbirdAddr, hbirdPort):
        gr.sync_block.__init__(self,
            name="HummingbirdToXMLRPC",
            in_sig=None,
            out_sig=None)
	self.xmlrpcAddr=xmlrpcAddr
	self.xmlrpcPort=xmlrpcPort
	self.hbirdAddr=hbirdAddr
	self.hbirdPort=hbirdPort

    def work(self, input_items, output_items):
	t=threading.Thread(target=self.receiveData)
	t.start()
        return

    def receiveData(self):

	ECCenterFrequency = 437505000
	correctFrequency = ECCenterFrequency

	#Setup xmlrpc client - sends doppler shift to GNURadio chain.
	sURL = "http://" + self.xmlrpcAddr + ":" + str(self.xmlrpcPort)
	s=xmlrpclib.ServerProxy(sURL)
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the port
	server_address = (self.hbirdAddr, self.hbirdPort)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	sock.bind(server_address)

	# Listen for incoming connections
	sock.listen(1)
	BUFFER_SIZE = 16

	while True:
	    # Wait for a connection
	    print >>sys.stderr, 'waiting for a connection'
	    connection, client_address = sock.accept()

	    try:
		print >>sys.stderr, 'connection from', client_address

		# Receive the data in small chunks and retransmit it
		while True:
		    
		    data = connection.recv(BUFFER_SIZE)
		    print >>sys.stderr, 'received "%s"' % data
		    
		    if data:
		        
		        if data.startswith("F"):
		            correctFrequency = float(data[2:])
		            dopplerShift = correctFrequency - ECCenterFrequency
		            
		            #send doppler with xmlrps server:
		            try:
		                s.set_doppler_shift(dopplerShift)
		            except socket.error, e:
		                # log the exception here
		                print >>sys.stderr, "Cannot connect to GNURadio chain, make sure that the chain is running.\nWaiting 5 seconds."             
				time.sleep(5)
		            
		            response = "RPRT 0"
		            print >>sys.stderr, 'sending successful response back to the client\n%s' % response
		            connection.sendall(response)
		        
		        #gpredict asks for the current radio frequency
		        elif data.startswith("f"):
			    response = str(int(correctFrequency))
		            print >>sys.stderr, 'sending requested frequency back to the client\n%s' % response
		            connection.sendall(response)
		    else:
		        print >>sys.stderr, 'no more data from', client_address
		        break
		    
	    finally:
		# Clean up the connection
		connection.close()
	return
