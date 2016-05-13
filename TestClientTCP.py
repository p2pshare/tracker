import socket
import Request

'''
    File name: TestClientTCP.py
    Author: Chenglong Wei, classId 82, 010396464
    Date created: 5/11/2016
    Date last modified: 5/12/2016
    Python Version: 2.7.10
    Functions: TCP Tracker test.
    '''

HOST, PORT = "localhost", 9999
data = "hello server"

# Create a socket (SOCK_STREAM means a UDP socket)
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    message1 = Request.Request(cmd="report_active", ip="10.12.13.14", port=1234)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(message1.to_json())
    print "Sent:     %s" % message1.to_json()
    # Receive data from the server
    received = sock.recv(1024)
    print "Received: %s" % received
    sock.close()

    message2 = Request.Request(cmd="report_chunk", ip="10.12.13.14", port=1234, share_id="aabbccdd",
                               chunk_id="xxyyzzww")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(message2.to_json())
    print "Sent:     %s" % message2.to_json()
    # Receive data from the server
    received = sock.recv(1024)
    print "Received: %s" % received
    sock.close()

    message3 = Request.Request(cmd="get_chunk_peers", share_id="aabbccdd", chunk_id="xxyyzzww")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(message3.to_json())
    print "Sent:     %s" % message3.to_json()
    # Receive data from the server
    received = sock.recv(1024)
    print "Received: %s" % received
    sock.close()

finally:
    sock.close()
