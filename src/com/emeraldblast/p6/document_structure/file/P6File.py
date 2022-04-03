import json

from com.emeraldblast.p6.document_structure.file.P6Files import P6Files
from com.emeraldblast.p6.document_structure.workbook.WorkbookJson import WorkbookJson


class P6File:
    def __init__(self, version:str, workbookJson:WorkbookJson):
        self.version:str = version
        self.workbookJson:WorkbookJson = workbookJson

    def toJsonDict(self):
        return {
            "version":self.version,
            "workbookJson":self.workbookJson.toJsonDictForSaving()
        }
    def __str__(self):
        return json.dumps(self.toJsonDict())

    @staticmethod
    def fromJsonDict(jsonDict:dict):
        version = jsonDict.get("version")
        if version is None:
            version = P6Files.currentVersion
        return P6File(
            version=version,
            workbookJson=WorkbookJson.fromJsonDict(jsonDict.get("workbookJson"))
        )
    @staticmethod
    def fromJsonStr(jsonStr:str):
        return P6File.fromJsonDict(json.loads(jsonStr))