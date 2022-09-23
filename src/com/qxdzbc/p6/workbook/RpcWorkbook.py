from functools import partial
from pathlib import Path
from typing import Union, Optional

from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.InternalRpcWorkbook import InternalRpcWorkbook
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.WorkbookWrapper import WorkbookWrapper
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.rpc.RpcUtils import RpcUtils
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.rpc.RpcErrors import RpcErrors
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.proto.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub


class RpcWorkbook(WorkbookWrapper):
    _serverDownReport = RpcErrors.RpcServerIsDown \
        .report("Can't get sheet count because rpc server is down.")
    _serverDownException = _serverDownReport.toException()

    @staticmethod
    def fromNameAndPath(
            name: str,
            path: Optional[Path] = None,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()
    ):
        return RpcWorkbook(
            wbKey = WorkbookKeyImp(name, path),
            stubProvider = stubProvider
        )

    def __init__(self, wbKey: WorkbookKey,
                 stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()):
        super().__init__(InternalRpcWorkbook(wbKey,stubProvider))
        self.__key = self.rootWorkbook.key
        self._stubProvider = stubProvider

    def __eq__(self, o: object) -> bool:
        if isinstance(o,Workbook):
            return self.key == o.key
        else:
            return False

    @property
    def _wbsv(self) -> Optional[WorkbookServiceStub]:
        return self._stubProvider.wbService

    ### >> Workbook << ###

    def removeAllWorksheetRs(self) -> Result[None, ErrorReport]:
        return self._onWbsvOkRs(self.rootWorkbook.removeAllWorksheetRs)

    @property
    def worksheets(self) -> list[Worksheet]:
        def f() -> list[Worksheet]:
            return self.rootWorkbook.worksheets
        return self._onWbsvOk(f)

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[Worksheet, ErrorReport]:
        return self._onWbsvOkRs(partial(
            self.rootWorkbook.setActiveWorksheetRs,indexOrName
        ))
    
    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        def f() -> Optional[Worksheet]:
            return self.rootWorkbook.activeWorksheet

        return self._onWbsvOk(f)

    def _onWbsvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self._wbsv,f)

    def _onWbsvOk(self, f):
        return RpcUtils.onServiceOkOrRaise(self._wbsv, f)

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorkbook.getWorksheetByNameRs,name))

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorkbook.getWorksheetByIndexRs,index))

    def getWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorkbook.getWorksheetRs, nameOrIndex))

    @property
    def wsCount(self) -> int:
        def f():
            return self.rootWorkbook.wsCount
        return self._onWbsvOk(f)

    @property
    def key(self) -> WorkbookKey:
        return self.rootWorkbook.key

    @key.setter
    def key(self, newKey: WorkbookKey):
        def f():
            self.rootWorkbook.key = newKey
        self._onWbsvOk(f)
        

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorkbook.createNewWorksheetRs,newSheetName))

    def removeWorksheetByNameRs(self, sheetName: str) -> Result[None, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorkbook.removeWorksheetByNameRs, sheetName))

    def removeWorksheetByIndexRs(self, index: int) -> Result[None, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorkbook.removeWorksheetByIndexRs, index))

    def addWorksheetRs(self, ws: Worksheet) -> Result[Worksheet, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorkbook.addWorksheetRs,ws))

    def renameWorksheetRs(self, oldName: str, newName: str) -> Result[None, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorkbook.renameWorksheetRs,oldName,newName))
