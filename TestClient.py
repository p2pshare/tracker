import socket

HOST, PORT = "localhost", 8888
data = "hello server"

# Create a socket (SOCK_STREAM means a UDP socket)
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     %s"%data
print "Received: %s"%received
