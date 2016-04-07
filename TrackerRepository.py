import redis


class TrackerRepository:
    '''Interact with redis database.'''

    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.r = redis.Redis(connection_pool=self.pool)

    def report_active(self, ip, port):
        self.r.set(self.get_active_peer_key(ip, port), "active", 5 * 60)

    def report_chunk(self, chunk_id, ip, port):
        self.r.sadd(self.get_chunk_key(chunk_id), self.get_peer_val(ip, port))

    def get_chunk_peers(self, chunk_id):
        peers = self.r.smembers(self.get_chunk_key(chunk_id))
        return filter(lambda peer: self.is_peer_active(peer), peers)

    def is_peer_active(self, peer):
        ip_port = peer.split("#")
        return self.r.exists(self.get_active_peer_key(ip_port[0], int(ip_port[1])))

    def get_chunk_key(self, chunk_id):
        return "chunk#" + chunk_id

    def get_peer_val(self, ip, port):
        return ip + "#" + str(port)

    def get_active_peer_key(self, ip, port):
        return "active_peer#" + self.get_peer_val(ip, port)

repo = TrackerRepository()
# test setup
repo.report_active("127.0.0.1", 1234)
repo.report_active("127.0.0.3", 1234)
repo.report_chunk("1001", "127.0.0.1", 1234)
repo.report_chunk("1001", "127.0.0.2", 1234)
repo.report_chunk("1001", "127.0.0.3", 1234)

# dup
repo.report_chunk("1001", "127.0.0.1", 1234)
repo.report_chunk("1001", "127.0.0.2", 1234)
repo.report_chunk("1001", "127.0.0.3", 1234)
print repo.get_chunk_peers("1001")

# test clean up
repo.r.delete(repo.get_active_peer_key("127.0.0.1", 1234))
repo.r.delete(repo.get_active_peer_key("127.0.0.3", 1234))
repo.r.delete(repo.get_chunk_key("1001"))
