import socket
import Request

HOST, PORT = "localhost", 8888
data = "hello server"

# Create a socket (SOCK_STREAM means a UDP socket)
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    message1 = Request.Request(cmd="report_active", ip="10.12.13.14", port=1234)
    message2 = Request.Request(cmd="report_chunk", ip="10.12.13.14", port=1234, share_id="aabbccdd", chunk_id="xxyyzzww")
    message3 = Request.Request(cmd="get_chunk_peers", share_id="aabbccdd", chunk_id="xxyyzzww")

    sock.sendall(message1.to_json())
    print "Sent:     %s"%message1.to_json()
    # Receive data from the server
    received = sock.recv(1024)
    print "Received: %s"%received

    sock.sendall(message2.to_json())
    print "Sent:     %s"%message2.to_json()
    # Receive data from the server
    received = sock.recv(1024)
    print "Received: %s"%received

    sock.sendall(message3.to_json())
    print "Sent:     %s"%message3.to_json()
    # Receive data from the server
    received = sock.recv(1024)
    print "Received: %s"%received

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     %s"%data
print "Received: %s"%received
