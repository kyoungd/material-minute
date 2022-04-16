class TestPublisher:
    def __init__(self, callback):
        self.callback = callback

    def publish(self, data):
        self.callback(data)
