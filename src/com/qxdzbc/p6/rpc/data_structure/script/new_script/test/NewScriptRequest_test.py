import unittest

from com.qxdzbc.p6.script.ScriptEntry import ScriptEntry
from com.qxdzbc.p6.script.ScriptEntryKey import ScriptEntryKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.script.new_script.NewScriptRequest import NewScriptRequest
from com.qxdzbc.p6.proto.ScriptProtos_pb2 import NewScriptRequestProto


class NewScriptRequest_test(unittest.TestCase):
    def test_fromProtoBytes_fromProto(self):
        entry = ScriptEntry(
            key = ScriptEntryKey(
                name = "s1",
                workbookKey = WorkbookKeys.fromNameAndPath("b1")
            ),
            script = "script content 1"
        )
        proto = NewScriptRequestProto(
            scriptEntry = entry.toProtoObj()
        )
        o = NewScriptRequest.fromProto(proto)
        self.assertEqual(entry, o.scriptEntry)
        o2 = NewScriptRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(entry, o2.scriptEntry)

if __name__ == '__main__':
    unittest.main()
