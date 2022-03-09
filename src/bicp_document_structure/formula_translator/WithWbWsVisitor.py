from bicp_document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor
from bicp_document_structure.formula_translator.antlr4.FormulaParser import FormulaParser
from bicp_document_structure.formula_translator.antlr4.FormulaVisitor import FormulaVisitor
from bicp_document_structure.formula_translator.mapper.PythonMapper import PythonMapper
from bicp_document_structure.formula_translator.mapper.WorkbookMapper import WorkbookMapper
from bicp_document_structure.formula_translator.mapper.WorksheetMapper import WorksheetMapper
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class WithWbWsVisitor(PythonFormulaVisitor):
    def __init__(self,
                 visitor: FormulaVisitor,
                 sheetName: str | None = None,
                 workbookKey: WorkbookKey | None = None
                 ):
        super().__init__()
        self._sheetName: str | None = sheetName
        self._wbKey: WorkbookKey | None = workbookKey
        self._visitor:FormulaVisitor = visitor
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
                getSheet = self.wbMapper.getSheet(sheetName)
            rt = f'{self.__getWBCode}.{getSheet}.{rangeObj}'
        else:
            if len(sheetName) != 0:
                getSheet = self.mapper.getSheet(sheetName)
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
        getSheet: str = f'{getWb}.getSheet("{sheetName}")'
        return getSheet