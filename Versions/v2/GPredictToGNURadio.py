import time
import sys
import socket
import xmlrpclib
import binascii

ECCenterFrequency = 437505000
correctFrequency = ECCenterFrequency

#Setup xmlrpc client - sends doppler shift to GNURadio chain.
sURL = "http://localhost:1234"
s=xmlrpclib.ServerProxy(sURL)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 4532)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
BUFFER_SIZE = 32

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            
            data = connection.recv(BUFFER_SIZE)
            #print >>sys.stderr, 'received "%s"' % data
            
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
                    
                    
                    #print >>sys.stderr, 'sending successful response back to the client'
                    connection.sendall('RPRT 0')
                
                #gpredict asks for the current radio frequency
                elif data.startswith("f"):
                    #print >>sys.stderr, 'sending requested frequency back to the client'
                    connection.sendall(str(int(correctFrequency)))
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()
