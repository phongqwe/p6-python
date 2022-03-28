from abc import ABC

class EventServer(ABC):

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
