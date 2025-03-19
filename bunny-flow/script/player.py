
class Player:
    id = NotImplemented
    stream_url = NotImplemented
    folder = NotImplemented

    def __init__(self, stream_url):
        self.stream_url = stream_url
        