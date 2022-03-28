from abc import ABC

class EventServer(ABC):
    """ A protocol-buffer server accepting requests and sending back responses """
    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
