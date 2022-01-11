import json


class RunResultJson(dict):
    """
    Json representation of a RunResult
    """
    def __init__(self, mutatedCells, deletedCells):
        super().__init__()
        self.mutatedCells = mutatedCells
        self.deletedCells = deletedCells

    def __str__(self):
        return json.dumps(self.__dict__)