from com.qxdzbc.p6.util.two_way_ref import TwoWayRef
from com.qxdzbc.p6.util.two_way_ref.TwoWayRefImp import TwoWayRefImp

from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


class Refs:
    @staticmethod
    def wbws(workbook:Workbook, worksheet:Worksheet)-> TwoWayRef[Workbook, Worksheet]:
        return TwoWayRefImp(workbook, worksheet)