class Result:

    @property
    def err(self):
        raise NotImplementedError()

    def value(self):
        raise NotImplementedError()

    def isOk(self):
        return self.value is not None

    def isErr(self):
        return self.err is not None

