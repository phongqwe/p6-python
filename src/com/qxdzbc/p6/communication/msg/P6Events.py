import inspect

from com.qxdzbc.p6.communication.msg.P6Event import P6Event
from com.qxdzbc.p6.app.rpc_data_structure.CreateNewWorkbookRequest import CreateNewWorkbookRequest
from com.qxdzbc.p6.app.rpc_data_structure.CreateNewWorkbookResponse import CreateNewWorkbookResponse
from com.qxdzbc.p6.app.rpc_data_structure.LoadWorkbookRequest import LoadWorkbookRequest
from com.qxdzbc.p6.app.rpc_data_structure.LoadWorkbookResponse import LoadWorkbookResponse
from com.qxdzbc.p6.app.rpc_data_structure.SetActiveWorksheetRequest import SetActiveWorksheetRequest
from com.qxdzbc.p6.app.rpc_data_structure.SetActiveWorksheetResponse import SetActiveWorksheetResponse
from com.qxdzbc.p6.cell.rpc_data_structure.CellMultiUpdateRequest import CellMultiUpdateRequest
from com.qxdzbc.p6.cell.rpc_data_structure.CellMultiUpdateResponse import CellMultiUpdateResponse
from com.qxdzbc.p6.cell.rpc_data_structure.CellUpdateRequest import CellUpdateRequest
from com.qxdzbc.p6.cell.rpc_data_structure.CellUpdateResponse import CellUpdateResponse
from com.qxdzbc.p6.range.rpc_data_structure.paste_range.PasteRangeRequest import PasteRangeRequest
from com.qxdzbc.p6.range.rpc_data_structure.paste_range import PasteRangeResponse
from com.qxdzbc.p6.range.rpc_data_structure.range_to_clipboard import \
    RangeToClipboardRequest
from com.qxdzbc.p6.range.rpc_data_structure.range_to_clipboard import \
    RangeToClipboardResponse
from com.qxdzbc.p6.script.rpc_data_structure.new_script.NewScriptRequest import NewScriptRequest
from com.qxdzbc.p6.script.rpc_data_structure.new_script.NewScriptResponse import NewScriptResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.CreateNewWorksheetResponse import \
    CreateNewWorksheetResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.DeleteWorksheetRequest import DeleteWorksheetRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.DeleteWorksheetResponse import DeleteWorksheetResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.RenameWorksheetRequest import RenameWorksheetRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.save_wb.SaveWorkbookRequest import SaveWorkbookRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.save_wb.SaveWorkbookResponse import SaveWorkbookResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.DeleteMultiRequest import DeleteMultiRequest
from com.qxdzbc.p6.worksheet.rpc_data_structure.DeleteMultiResponse import DeleteMultiResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.RenameWorksheetResponse import RenameWorksheetResponse

WSE = "WORKSHEET_EVENT"  # worksheet event
CE = "CELL_EVENT"  # cell event
RE = "RANGE_EVENT_"  # range event
WBE = "WORKBOOK_EVENT"  # workbook event
ESE = "ESE"  # event server event
APPE = "APP_EVENT_"  # app event
FBE = "FALL_BACK_EVENT_" 
SCRIPT_EVENT="SCRIPT_EVENT_"


class P6Events:

    @staticmethod
    def allEvents(groupName: str) -> list[P6Event]:
        rt = []
        for k in P6Events.__dict__:
            eventGroup = P6Events.__dict__[k]
            if k == groupName and inspect.isclass(eventGroup):
                for eventName in eventGroup.__dict__:
                    event = eventGroup.__dict__[eventName]
                    if inspect.isclass(event):
                        rt.append(event.event)
        return rt
    
    class Script:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class NewScript:
            event = P6Event(f"{SCRIPT_EVENT}1","new script event")
            Request = NewScriptRequest
            Response = NewScriptResponse
            Other = []

    class Cell:

        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class Common:
            event = P6Event(f"{CE}0", "common cell event")

        class Update:
            event = P6Event(f"{CE}1", "cell update")
            Response = CellUpdateResponse
            Request = CellUpdateRequest

        class MultiUpdate:
            event = P6Event(f"{CE}2", "cell multi update")
            Request = CellMultiUpdateRequest
            Response = CellMultiUpdateResponse

    class Worksheet:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class Common:
            event = P6Event(f"{WSE}0", "Workheet common event")

        class ReRun:
            event = P6Event(f"{WSE}1", "Worksheet rerun")

        class Rename:
            event = P6Event(f"{WSE}2", "rename worksheet")
            Response = RenameWorksheetResponse
            Request = RenameWorksheetRequest

        class DeleteCell:
            event = P6Event(f"{WSE}3", "Delete cell")

        class DeleteMulti:
            event = P6Event(f"{WSE}4", "Delete multi")
            Request = DeleteMultiRequest
            Response = DeleteMultiResponse

        # class PasteRange:
        #     event = P6Event(f"{WSE}5", "Paste range")

    class Range:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class ReRun:
            event = P6Event(f"{RE}0", "Range rerun")

        class RangeToClipBoard:
            event = P6Event(f"{RE}1", "Range to clipboard")
            Request = RangeToClipboardRequest
            Response = RangeToClipboardResponse
        class PasteRange:
            event = P6Event(f"{RE}2","Range to clipboard")
            Request=PasteRangeRequest
            Response = PasteRangeResponse

    class Workbook:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class Update:
            event = P6Event(f"{WBE}0", "Workbook update event")

        class ReRun:
            event = P6Event(f"{WBE}1", "Workbook rerun")


        class DeleteWorksheet:
            event = P6Event(f"{WBE}2", "remove worksheet")
            Request = DeleteWorksheetRequest
            Response = DeleteWorksheetResponse

        class CreateNewWorksheet:
            event = P6Event(f"{WBE}3", "create new worksheet")
            Response = CreateNewWorksheetResponse
            Request = CreateNewWorksheetRequest

    class EventServer:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class UnknownEvent:
            event = P6Event(f"{ESE}0", "Unknown event")

        class UnknownError:
            event = P6Event(f"{ESE}0", "Unknown error")

    class App:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class SetActiveWorksheet:
            event = P6Event(f"{APPE}0", "Set active worksheet")
            Request = SetActiveWorksheetRequest
            Response = SetActiveWorksheetResponse

        class SaveWorkbook:
            event = P6Event(f"{APPE}1", "save workbook")
            Request = SaveWorkbookRequest
            Response = SaveWorkbookResponse

        class LoadWorkbook:
            event = P6Event(f"{APPE}2", "load workbook")
            Request = LoadWorkbookRequest
            Response = LoadWorkbookResponse

        class CreateNewWorkbook:
            event = P6Event(f"{APPE}3", "create new workbook")
            Request = CreateNewWorkbookRequest
            Response = CreateNewWorkbookResponse

    class Fallback:
        class UnknownEvent:
            event = P6Event(f"{FBE}0", "Unknown event")