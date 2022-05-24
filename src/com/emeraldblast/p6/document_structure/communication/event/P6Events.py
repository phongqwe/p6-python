import inspect

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateRequest import \
    CellUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.CreateNewWorksheetData import \
    CreateNewWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetRequest import \
    RenameWorksheetRequest

WSE = "WSE"  # worksheet event
CE = "CE"  # cell event
RE = "RE"  # range event
WBE = "WBE"  # workbook event
ESE = "ESE"  # event server event
APPE = "APPE" # app event

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

    class Cell:

        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class Common:
            event = P6Event(f"{CE}0", "common cell event")

        class Update:
            event = P6Event(f"{CE}1", "cell update")
            Response = WorkbookUpdateCommonResponse
            Request = CellUpdateRequest

        class MultiUpdate:
            event = P6Event(f"{CE}2", "cell multi update")

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

    class Range:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class ReRun:
            event = P6Event(f"{RE}0", "Range rerun")

    class Workbook:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        class Common:
            event = P6Event(f"{WBE}0", "Workbook common event")

        class ReRun:
            event = P6Event(f"{WBE}1", "Workbook rerun")

        class DeleteWorksheet:
            event = P6Event(f"{WBE}2", "remove worksheet")

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
            event = P6Event(f"{ESE}0","Unknown error")

    class App:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)
        class SetActiveWorksheet:
            event = P6Event(f"{APPE}0","Set active worksheet")
        class SaveWorkbook:
            event = P6Event(f"{APPE}1","save workbook")

        class LoadWorkbook:
            event = P6Event(f"{APPE}2","load workbook")