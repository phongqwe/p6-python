import unittest

from com.qxdzbc.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.qxdzbc.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.qxdzbc.p6.new_architecture.data_structure import \
    NewScriptRequest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
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
