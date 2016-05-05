import json


class Response(object):
    '''
    File name: Response.py
    Author: Chenglong Wei, classId 82, 010396464
    Date created: 4/20/2016
    Date last modified: 5/1/2016
    Python Version: 2.7.10
    Functions: Wrapped peer's response.
    '''

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
