import unittest

from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.emeraldblast.p6.document_structure.communication.event.data_structure.script_event.new_script.NewScriptNotification import \
    NewScriptNotification


class NewScriptNotification_test(unittest.TestCase):
    def test_zz(self):
        notif = NewScriptNotification(
            scriptEntries = [],
            errorIndicator = ErrorIndicator.noError()
        )
        eventData = notif.toEventData()
        self.assertEqual(P6Events.Script.NewScript.event, eventData.event)


if __name__ == '__main__':
    unittest.main()
