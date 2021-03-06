import threading
import SocketServer
import TrackerService
import Request
import Response
import sys


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    '''
    File name: TrackerNetwork.py
    Author: Chenglong Wei, classId 82, 010396464
    Date created: 4/20/2016
    Date last modified: 5/1/2016
    Python Version: 2.7.10
    Functions: Get connection from peer, get peer's Request and response with data wrapped by Response.
               Use services provided by TrackerService.
    '''

    service = TrackerService.TrackerService()

    def handle(self):
        data = self.request[0].strip()
        # get port number
        port = self.client_address[1]
        # get the communicate socket
        socket = self.request[1]
        # get client host ip address
        client_address = (self.client_address[0])
        # proof of multithread
        cur_thread = threading.current_thread()
        print "thread %s" % cur_thread.name
        print "received call from client address :%s" % client_address
        print "received data from port [%s]: %s" % (port, data)

        # assemble a response message to client
        response = "%s %s" % (cur_thread.name, data)
        try:
            socket.sendto(self.get_response(Request.Request(js=data)).to_json(), self.client_address)
        except:
            e = sys.exc_info()[0]
            socket.sendto(Response.Response(message="FAIL", data=str(e)).to_json(), self.client_address)

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


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


if __name__ == "__main__":
    # in this example, we will bind port to 8888
    # for client connection
    HOST, PORT = "localhost", 8888

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address
    server.serve_forever()
    # Start a thread with the server --
    # that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    server.shutdown()
