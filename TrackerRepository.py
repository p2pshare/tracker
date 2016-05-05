import redis
import json


class TrackerRepository(object):
    '''
    File name: TrackerRepository.py
    Author: Chenglong Wei, classId 82, 010396464
    Date created: 4/1/2016
    Date last modified: 5/1/2016
    Python Version: 2.7.10
    Functions: Provide services to TrackerService.
               Interact with Redis database.
    '''

    def __init__(self):
        # From ConnectionPool get a connection.
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.r = redis.Redis(connection_pool=self.pool)

    def report_active(self, ip, port):
        # A peer report active state, the active state keep alive for 5 minutes.
        self.r.set(self.get_active_peer_key(ip, port), "active", 5 * 60)

    def report_chunk(self, share_id, chunk_id, ip, port):
        # A peer report chunk, save in Redis. Set is used to remove duplicates.
        self.r.sadd(self.get_chunk_key(share_id, chunk_id), self.get_peer_val(ip, port))

    def get_chunk_peers(self, share_id, chunk_id):
        chunk_key = self.get_chunk_key(share_id, chunk_id)
        # Get legacy peers that contain the chunk.
        legacy_peers = self.r.smembers(chunk_key)
        # We should only return active peers that contain the chunk.
        active_peers = filter(lambda peer: self.is_peer_active(peer), legacy_peers)

        # Remove dead peers that contain the trunk, to minimize the trunk peers set.
        for dead_peer in legacy_peers - set(active_peers):
            self.r.srem(chunk_key, dead_peer)

        return active_peers

    def is_peer_active(self, peer):
        # Tell whether a peer is active.
        ip_port = peer.split(":")
        return self.r.exists(self.get_active_peer_key(ip_port[0], ip_port[1]))

    def get_chunk_key(self, share_id, chunk_id):
        # Helper function to get chunk key.
        return "chunk#{share_id}#{chunk_id}".format(share_id=share_id, chunk_id=chunk_id)

    def get_peer_val(self, ip, port):
        # Helper function to get peer val.
        return "{ip}:{port}".format(ip=ip, port=port)

    def get_active_peer_key(self, ip, port):
        # Helper function to get active peer key.
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

print json.dumps(repo.get_chunk_peers("fdef", "1001"))

# test clean up
repo.r.delete(repo.get_active_peer_key("127.0.0.1", 1234))
repo.r.delete(repo.get_active_peer_key("127.0.0.3", 1234))
repo.r.delete(repo.get_chunk_key("fdef", "1001"))
