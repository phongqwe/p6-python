import inspect

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.paste_range.PasteRangeRequest import \
    PasteRangeRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.paste_range.PasteRangeResponse import \
    PasteRangeResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.script_event.new_script.NewScriptRequest import \
    NewScriptRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.script_event.new_script.NewScriptResponse import \
    NewScriptResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.CloseWorkbookReactor import \
    CloseWorkbookReactor

from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.CreateNewWorkbookReactor import \
    CreateNewWorkbookReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.LoadWorkbookReactor import \
    LoadWorkbookReactor

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.CloseWorkbookRequest import \
    CloseWorkbookRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.CloseWorkbookResponse import \
    CloseWorkbookResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.CreateNewWorkbookRequest import \
    CreateNewWorkbookRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.CreateNewWorkbookResponse import \
    CreateNewWorkbookResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.LoadWorkbookRequest import \
    LoadWorkbookRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.LoadWorkbookResponse import \
    LoadWorkbookResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.SetActiveWorksheetRequest import \
    SetActiveWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.SetActiveWorksheetResponse import \
    SetActiveWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellMultiUpdateRequest import \
    CellMultiUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellMultiUpdateResponse import \
    CellMultiUpdateResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateRequest import \
    CellUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateResponse import \
    CellUpdateResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.range_to_clipboard.RangeToClipboardRequest import \
    RangeToClipboardRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.range_to_clipboard.RangeToClipboardResponse import \
    RangeToClipboardResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.CreateNewWorksheetResponse import \
    CreateNewWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.DeleteWorksheetRequest import \
    DeleteWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.DeleteWorksheetResponse import \
    DeleteWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookRequest import \
    SaveWorkbookRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookResponse import \
    SaveWorkbookResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiRequest import \
    DeleteMultiRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiResponse import \
    DeleteMultiResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetRequest import \
    RenameWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.SaveWorkbookReactor import \
    SaveWorkbookReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.SetActiveWorksheetReactor import \
    SetActiveWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.cell_event.CellMultiUpdateReactor import \
    CellMultiUpdateReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.cell_event.CellUpdateReactor import \
    CellUpdateReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.range_event.PasteRangeReactor import \
    PasteRangeReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.range_event.RangeToClipboardReactor import \
    RangeToClipboardReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.script_event.new_script.NewScriptReactor import \
    NewScriptReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook_event.CreateNewWorksheetReactor import \
    CreateNewWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook_event.DeleteWorksheetReactor import \
    DeleteWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.worksheet_event.DeleteMultiReactor import \
    DeleteMultiReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.worksheet_event.RenameWorksheetReactor import \
    RenameWorksheetReactor

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
        class NewScript:
            event = P6Event(f"{SCRIPT_EVENT}0","new script event")
            Request = NewScriptRequest
            Response = NewScriptResponse
            Reactor = NewScriptReactor

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
            Reactor = CellUpdateReactor

        class MultiUpdate:
            event = P6Event(f"{CE}2", "cell multi update")
            Request = CellMultiUpdateRequest
            Response = CellMultiUpdateResponse
            Reactor = CellMultiUpdateReactor

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
            Reactor = RenameWorksheetReactor

        class DeleteCell:
            event = P6Event(f"{WSE}3", "Delete cell")

        class DeleteMulti:
            event = P6Event(f"{WSE}4", "Delete multi")
            Request = DeleteMultiRequest
            Response = DeleteMultiResponse
            Reactor = DeleteMultiReactor

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
            Reactor = RangeToClipboardReactor
        class PasteRange:
            event = P6Event(f"{RE}2","Range to clipboard")
            Request=PasteRangeRequest
            Response = PasteRangeResponse
            Reactor = PasteRangeReactor

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
            Reactor = DeleteWorksheetReactor

        class CreateNewWorksheet:
            event = P6Event(f"{WBE}3", "create new worksheet")
            Response = CreateNewWorksheetResponse
            Request = CreateNewWorksheetRequest
            Reactor = CreateNewWorksheetReactor

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
            Reactor = SetActiveWorksheetReactor

        class SaveWorkbook:
            event = P6Event(f"{APPE}1", "save workbook")
            Request = SaveWorkbookRequest
            Response = SaveWorkbookResponse
            Reactor = SaveWorkbookReactor

        class LoadWorkbook:
            event = P6Event(f"{APPE}2", "load workbook")
            Request = LoadWorkbookRequest
            Response = LoadWorkbookResponse
            Reactor =LoadWorkbookReactor

        class CreateNewWorkbook:
            event = P6Event(f"{APPE}3", "create new workbook")
            Request = CreateNewWorkbookRequest
            Response = CreateNewWorkbookResponse
            Reactor = CreateNewWorkbookReactor

        class CloseWorkbook:
            event = P6Event(f"{APPE}4", "close workbook")
            Request = CloseWorkbookRequest
            Response = CloseWorkbookResponse
            Reactor = CloseWorkbookReactor

    class Fallback:
        class UnknownEvent:
            event = P6Event(f"{FBE}0", "Unknown event")