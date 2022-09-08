import unittest

from com.qxdzbc.p6.new_architecture.communication import P6Events
from com.qxdzbc.p6.new_architecture.rpc.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.qxdzbc.p6.new_architecture.rpc.data_structure.script_event.new_script.NewScriptNotification import \
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
