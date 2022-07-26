from typing import Optional

from com.emeraldblast.p6.document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor
from com.emeraldblast.p6.document_structure.formula_translator.antlr4.FormulaParser import FormulaParser
from com.emeraldblast.p6.document_structure.formula_translator.mapper.PythonMapper import PythonMapper
from com.emeraldblast.p6.document_structure.formula_translator.mapper.WorkbookMapper import WorkbookMapper
from com.emeraldblast.p6.document_structure.formula_translator.mapper.WorksheetMapper import WorksheetMapper
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class WbWsVisitor(PythonFormulaVisitor):
    def __init__(self,
                 sheetName: Optional[str] = None,
                 workbookKey: WorkbookKey | None = None
                 ):
        super().__init__()
        self._sheetName: Optional[str] = sheetName
        self._wbKey: WorkbookKey | None = workbookKey
        self.mapper = PythonMapper.instance()
        self.wsMapper = WorksheetMapper.instance()
        self.wbMapper = WorkbookMapper.instance()
        self.getSheetCode:str = self.__getSheet(self._sheetName)
        self.__getWBCode:str = self.mapper.getWorkbook(self._wbKey)

    def visitSheetRangeAddrExpr(self, ctx: FormulaParser.SheetRangeAddrExprContext):
        rawSheetName = ""
        if ctx.SHEET_PREFIX() is not None:
            rawSheetName = ctx.SHEET_PREFIX().getText()
        else:
            if self._sheetName is not None:
                rawSheetName = self._sheetName
        sheetName: str = self._extractSheetName(rawSheetName)  # specific
        getSheet: str = ""
        rangeObj = self.visit(ctx.rangeAddress())
        if self.__getWBCode is not None:
            if len(sheetName) != 0:
                getSheet = self.wbMapper.getWorksheet(sheetName)
            rt = f'{self.__getWBCode}.{getSheet}.{rangeObj}'
        else:
            if len(sheetName) != 0:
                getSheet = self.mapper.getWorksheet(sheetName)
            rt = f'{getSheet}.{rangeObj}'
        return rt

    def visitPairCellAddress(self, ctx: FormulaParser.PairCellAddressContext):
        cell0 = ctx.cellAddress(0).getText()
        cell1 = ctx.cellAddress(1).getText()
        rangeAddress = self.mapper.formatRangeAddress(f'{cell0}:{cell1}')
        if self._sheetName is None:
            return self.mapper.getRange(rangeAddress)
        else:
            return self.wsMapper.getRange(rangeAddress)

    def visitOneCellAddress(self, ctx: FormulaParser.OneCellAddressContext):
        cellAddress = self.mapper.formatRangeAddress(ctx.cellAddress().getText())
        if self._sheetName is None:
            return self.mapper.getCell(cellAddress) + ".value"
        else:
            return self.wsMapper.getCell(cellAddress) + ".value"
        

    def visitColAddress(self, ctx: FormulaParser.ColAddressContext):
        if self._sheetName is None:
            return self.mapper.getRange(self.mapper.formatRangeAddress(ctx.getText()))
        else:
            return self.wsMapper.getRange(self.mapper.formatRangeAddress(ctx.getText()))
        
    def visitRowAddress(self, ctx: FormulaParser.RowAddressContext):
        if self._sheetName is None:
            return self.mapper.getRange(self.mapper.formatRangeAddress(ctx.getText()))
        else:
            return self.wsMapper.getRange(self.mapper.formatRangeAddress(ctx.getText()))


    def __getSheet(self, sheetName: str) -> str:
        if self._wbKey is None:
            getWb: str = self.mapper.getActiveWorkbook()
        else:
            getWb: str = self.mapper.getWorkbook(self._wbKey)
        getSheet: str = f'{getWb}.getWorksheet("{sheetName}")'
        return getSheet