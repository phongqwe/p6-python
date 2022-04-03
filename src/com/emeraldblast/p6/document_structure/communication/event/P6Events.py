from com.emeraldblast.p6.document_structure.communication.event.data.request.CellUpdateRequest import CellUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event.data.request.CreateNewWorksheetRequest import CreateNewWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data.request.RenameWorksheetRequest import RenameWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data.response.CellUpdateCommonResponse import CellUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.event.data.response.CreateNewWorksheetData import CreateNewWorksheetResponseData
from com.emeraldblast.p6.document_structure.communication.event.data.response.RenameWorksheetData import RenameWorksheetResponseData

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.event.MsgType import MsgType

WSE = "WSE" # worksheet event
CE = "CE" # cell event
RE = "RE" # range event
WBE = "WBE" # workbook event
ESE = "ESE" # event server event
class P6Events:
    class Cell:
        class UpdateValue:
            event = P6Event(f"{CE}0", MsgType.CellUpdateValue.value)
        UpdateValueEvent = UpdateValue.event

        UpdateScriptEvent = P6Event(f"{CE}1", MsgType.CellUpdateScript.value)
        UpdateFormula = P6Event(f"{CE}2", MsgType.CellUpdateFormula.value)
        ClearScriptResultEvent = P6Event(f"{CE}3", MsgType.CellClearScriptResult.value)

        class Update:
            event = P6Event(f"{CE}4", "cell update")
            Response = CellUpdateCommonResponse
            Request = CellUpdateRequest

    class Worksheet:
        ReRun = P6Event(f"{WSE}0", MsgType.WorksheetReRun.value)
        class Rename:
            event = P6Event(f"{WSE}1","rename worksheet")
            Response = RenameWorksheetResponseData
            Request = RenameWorksheetRequest



    class Range:
        ReRun = P6Event(f"{RE}0",MsgType.RangeReRun.value)

    class Workbook:
        ReRun = P6Event(f"{WBE}0",MsgType.WorkbookReRun.value)
        RemoveWorksheet = P6Event(f"{WBE}1","remove worksheet")
        class CreateNewWorksheet:
            event = P6Event(f"{WBE}3","create new worksheet")
            Response = CreateNewWorksheetResponseData
            Request = CreateNewWorksheetRequest

    class EventServer:
        Unknown = P6Event(f"{ESE}0", "Unknown event")
