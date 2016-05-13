import threading
import SocketServer
import TrackerService
import Request
import Response
import sys


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    '''
    File name: TrackerNetworkTCP.py
    Author: Chenglong Wei, classId 82, 010396464
    Date created: 5/11/2016
    Date last modified: 5/12/2016
    Python Version: 2.7.10
    Functions: TCP version of tracker server
               Get connection from peer, get peer's Request and response with data wrapped by Response.
               Use services provided by TrackerService.
    '''

    service = TrackerService.TrackerService()

    def handle(self):
        # get port number
        port = self.client_address[1]
        # get client host ip address
        client_address = (self.client_address[0])
        # proof of multithread
        cur_thread = threading.current_thread()
        print "thread %s" % cur_thread.name
        print "received call from client address :%s" % client_address

        try:
            data = self.request.recv(1024)
            self.request.sendall(self.get_response(Request.Request(js=data)).to_json())
        except:
            e = sys.exc_info()[0]
            self.request.sendall(Response.Response(message="FAIL", data=str(e)).to_json())

    def get_response(self, request):
        # Distinguish request type, and response with corresponding Response.
        if request.cmd == 'report_active':
            self.service.report_active(ip=request.ip, port=request.port)
            return Response.Response(message="OK")
        elif request.cmd == 'report_chunk':
            self.service.report_chunk(share_id=request.share_id, chunk_id=request.chunk_id, ip=request.ip,
                                      port=request.port)
            return Response.Response(message="OK")
        elif request.cmd == 'get_chunk_peers':
            response = Response.Response(message="OK")
            response.data = self.service.get_chunk_peers(share_id=request.share_id, chunk_id=request.chunk_id)
            return response
        else:
            return Response.Response(message="FAIL", data="cmd not recognized!")


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.serve_forever()
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    server.shutdown()
    server.server_close()
