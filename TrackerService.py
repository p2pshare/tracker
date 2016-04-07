import TrackerRepository


class TrackerService:
    def __init__(self):
        self.repo = TrackerRepository.TrackerRepository()

    def report_active(self, ip, port):
        self.repo.report_active(ip, port)

    def report_chunk(self, chunk_id, ip, port):
        self.repo.report_chunk(chunk_id, ip, port)

    def get_chunk_peers(self, chunk_id):
        return self.repo.get_chunk_peers(chunk_id)


trackService = TrackerService()
# test setup
trackService.report_active("127.0.0.1", 1234)
trackService.report_active("127.0.0.3", 1234)
trackService.report_chunk("1001", "127.0.0.1", 1234)
trackService.report_chunk("1001", "127.0.0.2", 1234)
trackService.report_chunk("1001", "127.0.0.3", 1234)

# dup
trackService.report_chunk("1001", "127.0.0.1", 1234)
trackService.report_chunk("1001", "127.0.0.2", 1234)
trackService.report_chunk("1001", "127.0.0.3", 1234)
print trackService.get_chunk_peers("1001")

# test clean up
trackService.repo.r.delete(trackService.repo.get_active_peer_key("127.0.0.1", 1234))
trackService.repo.r.delete(trackService.repo.get_active_peer_key("127.0.0.3", 1234))
trackService.repo.r.delete(trackService.repo.get_chunk_key("1001"))
