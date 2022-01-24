import json
from typing import List

from bicp_document_structure.cell.CellJson import CellJson


class WorksheetJson(dict):
    def __init__(self, name: str, cells: List[CellJson]):
        super().__init__()
        self.name = name
        self.cells = cells

    def __str__(self):
        return json.dumps(self.toJsonDict())

    def toJsonDict(self):
        cellDicts = []
        for cell in self.cells:
            cellDicts.append(cell.toJsonDict())
        return ({
            "name": self.name,
            "cells": cellDicts
        })

    @staticmethod
    def fromJsonDict(jsonDict: dict):
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
        d = json.loads(jsonStr)
        return WorksheetJson.fromJsonDict(d)
