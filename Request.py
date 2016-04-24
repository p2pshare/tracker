import json


class Request(object):
    def __init__(self, js=None, cmd=None, ip=None, port=None, share_id=None, chunk_id=None):
        if js is not None:
            self.__dict__ = json.loads(js)
            return

        self.cmd = cmd
        self.ip = ip
        self.port = port
        self.share_id = share_id
        self.chunk_id = chunk_id

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


message1 = Request(cmd="report_active", ip="10.12.13.14", port=1234)
print (message1.to_json())
message2 = Request(cmd="report_chunk", ip="10.12.13.14", port=1234, share_id="aabbccdd", chunk_id="xxyyzzww")
print (message2.to_json())
message3 = Request(cmd="get_chunk_peers", share_id="aabbccdd", chunk_id="xxyyzzww")
print (message3.to_json())

message4 = Request(js='{"ip": "10.12.13.14", "cmd": "report_chunk", "share_id": "aabbccdd", '
                   '"port": 1234, "chunk_id": "xxyyzzww"}')
print message4.to_json()
