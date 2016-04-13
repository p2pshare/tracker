import redis


class TrackerRepository(object):
    '''Interact with redis database.'''

    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.r = redis.Redis(connection_pool=self.pool)

    def report_active(self, ip, port):
        self.r.set(self.get_active_peer_key(ip, port), "active", 5 * 60)

    def report_chunk(self, share_id, chunk_id, ip, port):
        self.r.sadd(self.get_chunk_key(share_id, chunk_id), self.get_peer_val(ip, port))

    def get_chunk_peers(self, share_id, chunk_id):
        chunk_key = self.get_chunk_key(share_id, chunk_id)
        legacy_peers = self.r.smembers(chunk_key)
        active_peers = filter(lambda peer: self.is_peer_active(peer), legacy_peers)

        for dead_peer in legacy_peers - set(active_peers):
            self.r.srem(chunk_key, dead_peer)

        return active_peers

    def is_peer_active(self, peer):
        ip_port = peer.split("#")
        return self.r.exists(self.get_active_peer_key(ip_port[0], ip_port[1]))

    def get_chunk_key(self, share_id, chunk_id):
        return "chunk#{share_id}#{chunk_id}".format(share_id=share_id, chunk_id=chunk_id)

    def get_peer_val(self, ip, port):
        return "{ip}#{port}".format(ip=ip, port=port)

    def get_active_peer_key(self, ip, port):
        return "active_peer#{peer_val}".format(peer_val=self.get_peer_val(ip, port))


repo = TrackerRepository()
# test setup
repo.report_active("127.0.0.1", 1234)
repo.report_active("127.0.0.3", 1234)
repo.report_chunk("fdef", "1001", "127.0.0.1", 1234)
repo.report_chunk("fdef", "1001", "127.0.0.2", 1234)
repo.report_chunk("fdef", "1001", "127.0.0.3", 1234)

# dup
repo.report_chunk("fdef", "1001", "127.0.0.1", 1234)
repo.report_chunk("fdef", "1001", "127.0.0.2", 1234)
repo.report_chunk("fdef", "1001", "127.0.0.3", 1234)

print repo.get_chunk_peers("fdef", "1001")

# test clean up
repo.r.delete(repo.get_active_peer_key("127.0.0.1", 1234))
repo.r.delete(repo.get_active_peer_key("127.0.0.3", 1234))
repo.r.delete(repo.get_chunk_key("fdef", "1001"))
