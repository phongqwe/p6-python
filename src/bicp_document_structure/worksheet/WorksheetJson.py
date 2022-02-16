import json
from typing import List

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.common.ToJsonStr import ToJson


class WorksheetJson(dict, ToJson):
    """
    json representation of a Worksheet.
    str(WorksheetJson) returns the equivalent json string.
    """
    def __init__(self, name: str, cells: List[CellJson]):
        super().__init__()
        self.name = name
        self.cells = cells

    @staticmethod
    def fromJsonDict(jsonDict: dict):
        """create an instance of this class from a dict"""
        cells = []
        for cell in jsonDict.get("cells"):
            cellJson = CellJson.fromJsonDict(cell)
            cells.append(cellJson)
        return WorksheetJson(
            name=jsonDict.get("name"),
            cells=cells
        )

    @staticmethod
    def fromJsonStr(jsonStr: str):
        """create an instance of this class from a json string"""
        d = json.loads(jsonStr)
        return WorksheetJson.fromJsonDict(d)

    def toJsonStr(self) -> str:
        return str(self)

    def __str__(self):
        return json.dumps(self.toJsonDict())

    def toJsonDict(self):
        """convert this object into a dict """
        cellDicts = []
        for cell in self.cells:
            cellDicts.append(cell.toJsonDict())
        return ({
            "name": self.name,
            "cells": cellDicts
        })