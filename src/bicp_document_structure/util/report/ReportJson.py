import json


class ReportJson(dict):
    def __init__(self, isOk: bool, message: str, data:dict):
        super().__init__()
        self.isOk = isOk
        self.message = message
        self.data = data
    def __str__(self):
        return json.dumps(self.__dict__)