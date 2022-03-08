from bicp_document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor
from bicp_document_structure.formula_translator.antlr4.FormulaParser import FormulaParser
from bicp_document_structure.formula_translator.antlr4.FormulaVisitor import FormulaVisitor
from bicp_document_structure.formula_translator.mapper.PythonMapper import PythonMapper
from bicp_document_structure.formula_translator.mapper.WorkbookMapper import WorkbookMapper
from bicp_document_structure.formula_translator.mapper.WorksheetMapper import WorksheetMapper
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class WithWbWsVisitor(PythonFormulaVisitor):
    def __init__(self,
                 sheetName: str,
                 workbookKey: WorkbookKey,
                 visitor: FormulaVisitor,):
        super().__init__()
        self._sheetName = sheetName
        self._wbKey = workbookKey
        self._visitor = visitor
        self.mapper = PythonMapper.instance()
        self.wsMapper = WorksheetMapper.instance()
        self.wbMapper = WorkbookMapper.instance()
        self.getSheetCode = self.__getSheet(self._sheetName)
        self.__getWBCode = self.mapper.getWorkbook(self._wbKey)

    def visitSheetRangeAddrExpr(self, ctx: FormulaParser.SheetRangeAddrExprContext):
        if ctx.SHEET_PREFIX() is not None:
            rawSheetName = ctx.SHEET_PREFIX().getText()
        else:
            rawSheetName = self._sheetName
        sheetName: str = self._extractSheetName(rawSheetName) # specific
        getSheet: str = ""
        if len(sheetName) != 0:
            getSheet = self.wbMapper.getSheet(sheetName)
        rangeObj = self.visit(ctx.rangeAddress())
        rt= f'{self.__getWBCode}.{getSheet}.{rangeObj}'
        return rt

    def visitPairCellAddress(self, ctx: FormulaParser.PairCellAddressContext):
        cell0 = ctx.cellAddress(0).getText()
        cell1 = ctx.cellAddress(1).getText()
        rangeAddress = self.mapper.formatRangeAddress(f'{cell0}:{cell1}')
        return self.wsMapper.getRange(rangeAddress)

    def visitOneCellAddress(self, ctx: FormulaParser.OneCellAddressContext):
        cellAddress = self.mapper.formatRangeAddress(ctx.cellAddress().getText())
        return self.wsMapper.getCell(cellAddress) + ".value"

    def visitColAddress(self, ctx: FormulaParser.ColAddressContext):
        return self.wsMapper.getRange(self.mapper.formatRangeAddress(ctx.getText()))

    def visitRowAddress(self, ctx: FormulaParser.RowAddressContext):
        return self.wsMapper.getRange(self.mapper.formatRangeAddress(ctx.getText()))


    def __getSheet(self,sheetName:str)->str:
        getWb:str = self.mapper.getWorkbook(self._wbKey)
        getSheet:str = f'{getWb}.getSheet("{sheetName}")'
        return getSheet

    def __getRange(self,getRangeCode:str)->str:
        getSheet = self.wbMapper.getSheet(self._sheetName)
        rt = f'{self.__getWBCode}.{getSheet}.{getRangeCode}'
        return rt