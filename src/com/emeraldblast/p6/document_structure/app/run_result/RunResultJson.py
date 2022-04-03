import json


class RunResultJson:
    """
    Json representation of a RunResult
    """
    def __init__(self, mutatedCellDict, deletedCellDict):
        self.mutated = mutatedCellDict
        self.deleted = deletedCellDict

    def __str__(self):
        return json.dumps(self.__dict__)