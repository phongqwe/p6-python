import unittest

from com.qxdzbc.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.qxdzbc.p6.document_structure.util.CommonError import CommonErrors
from com.qxdzbc.p6.proto.CommonProtos_pb2 import ErrorIndicatorProto


class ErrorIndicator_test(unittest.TestCase):
    def test_toProto(self):
        o = ErrorIndicator(
            isError = True,
            errorReport = CommonErrors.CommonError
        )
        p = o.toProtoObj()
        expect = ErrorIndicatorProto(
            isError = True,
            errorReport = CommonErrors.CommonError.toProtoObj()
        )
        self.assertEqual(expect,p)

    def test_toProto2(self):
        o = ErrorIndicator(
            isError = False,
            errorReport = None
        )
        p = o.toProtoObj()
        expect = ErrorIndicatorProto(
            isError = False,
        )
        self.assertEqual(expect, p)


if __name__ == '__main__':
    unittest.main()
