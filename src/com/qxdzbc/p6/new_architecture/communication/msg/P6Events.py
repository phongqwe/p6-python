import inspect

from com.qxdzbc.p6.new_architecture.communication.msg.P6Event import P6Event
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.CreateNewWorkbookRequest import CreateNewWorkbookRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.CreateNewWorkbookResponse import CreateNewWorkbookResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.LoadWorkbookRequest import LoadWorkbookRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.LoadWorkbookResponse import LoadWorkbookResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.SetActiveWorksheetRequest import SetActiveWorksheetRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.SetActiveWorksheetResponse import SetActiveWorksheetResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.cell.CellMultiUpdateRequest import CellMultiUpdateRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.cell.CellMultiUpdateResponse import CellMultiUpdateResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.cell.CellUpdateRequest import CellUpdateRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.cell.CellUpdateResponse import CellUpdateResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range.paste_range.PasteRangeRequest import PasteRangeRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range.paste_range.PasteRangeResponse import PasteRangeResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range.range_to_clipboard.RangeToClipboardRequest import \
    RangeToClipboardRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range.range_to_clipboard.RangeToClipboardResponse import \
    RangeToClipboardResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.script.new_script.NewScriptRequest import NewScriptRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.script.new_script.NewScriptResponse import NewScriptResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.CreateNewWorksheetResponse import \
    CreateNewWorksheetResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.DeleteWorksheetRequest import DeleteWorksheetRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.DeleteWorksheetResponse import DeleteWorksheetResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.RenameWorksheetRequest import RenameWorksheetRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.save_wb.SaveWorkbookRequest import SaveWorkbookRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.save_wb.SaveWorkbookResponse import SaveWorkbookResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.worksheet.DeleteMultiRequest import DeleteMultiRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.worksheet.DeleteMultiResponse import DeleteMultiResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.RenameWorksheetResponse import RenameWorksheetResponse

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