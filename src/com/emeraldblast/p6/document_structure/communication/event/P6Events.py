import inspect

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.event.data.request.CellUpdateRequest import CellUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event.data.request.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data.request.RenameWorksheetRequest import \
    RenameWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data.response.CellUpdateCommonResponse import \
    CellUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.event.data.response.CreateNewWorksheetData import \
    CreateNewWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data.response.DeleteWorksheetResponse import \
    DeleteWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data.response.RenameWorksheetData import \
    RenameWorksheetResponseData

WSE = "WSE"  # worksheet event
CE = "CE"  # cell event
RE = "RE"  # range event
WBE = "WBE"  # workbook event
ESE = "ESE"  # event server event


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
            Response = CellUpdateCommonResponse
            Request = CellUpdateRequest

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
            Response = RenameWorksheetResponseData
            Request = RenameWorksheetRequest

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

        class RemoveWorksheet:
            event = P6Event(f"{WBE}2", "remove worksheet")

        class CreateNewWorksheet:
            event = P6Event(f"{WBE}3", "create new worksheet")
            Response = CreateNewWorksheetResponse
            Request = CreateNewWorksheetRequest

    class EventServer:
        @classmethod
        def allEvents(clazz):
            return P6Events.allEvents(clazz.__name__)

        Unknown = P6Event(f"{ESE}0", "Unknown event")
