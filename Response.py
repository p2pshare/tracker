import json


class Response(object):
    def __init__(self, js=None, message=None, data=None):
        if js is not None:
            self.__dict__ = json.loads(js)
            return

        self.message = message
        self.data = data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


response1 = Response(message="OK")
print (response1.to_json())
response2 = Response(message="OK", data=["127.0.0.1:1234", "127.0.0.3:1234"])
print (response2.to_json())
