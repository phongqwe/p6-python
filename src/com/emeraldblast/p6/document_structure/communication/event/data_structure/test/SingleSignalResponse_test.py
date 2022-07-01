import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.emeraldblast.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse


class SingleSignalResponse_test(unittest.TestCase):
    def test_ToProto_FromProto(self):
        o = SingleSignalResponse(
            errIndicator = ErrorIndicator(
                isError = False,
            )
        )
        proto = o.toProtoObj()
        self.assertEqual(o.errIndicator.toProtoObj(), proto.errIndicator)
        o2 = SingleSignalResponse.fromProto(proto)
        self.assertEqual(o,o2)
    
        


if __name__ == '__main__':
    unittest.main()
