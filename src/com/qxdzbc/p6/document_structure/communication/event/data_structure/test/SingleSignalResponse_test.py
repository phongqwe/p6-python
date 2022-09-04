import unittest

from com.qxdzbc.p6.document_structure.util.for_test import TestUtils

from com.qxdzbc.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.qxdzbc.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse


class SingleSignalResponse_test(unittest.TestCase):
    def test_ToProto_FromProto(self):
        o = SingleSignalResponse(
            errorReport = TestUtils.TestErrorReport
        )
        proto = o.toProtoObj()
        self.assertEqual(o.errorReport.toProtoObj(), proto.errorReport)
        o2:SingleSignalResponse = SingleSignalResponse.fromProto(proto)
        self.assertTrue(o.errorReport.isSameErr(o2.errorReport))
    
        


if __name__ == '__main__':
    unittest.main()
