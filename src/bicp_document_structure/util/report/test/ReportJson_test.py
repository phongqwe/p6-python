import json
import unittest

from bicp_document_structure.util.JsonStrMaker import JsonStrMaker
from bicp_document_structure.util.report.ReportJson import ReportJson
from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok


class A:
    def __init__(self):
        self.x = 123
        self.y = "abc qqqq"

    def __str__(self):
        return json.dumps(self.__dict__)


class B(JsonStrMaker):
    def __init__(self):
        self.x = 123
        self.y = "abc qqqq"

    def jsonStr(self) -> str:
        return json.dumps(self.__dict__)

    def __int__(self):
        return "not ok"


class ReportJson_test(unittest.TestCase):
    def test_toJson(self):
        r = ReportJson(True, "a message", json.dumps({
            "a": 1,
            "b": "b2"
        }))
        self.assertEqual("""{"isOk": true, "message": "a message", "data": "{\\\"a\\\": 1, \\\"b\\\": \\\"b2\\\"}"}""",
                         str(r))

    def test_fromOkResult(self):
        r = ReportJson.fromResultWithErrorReport(Ok("a data piece"))
        self.assertEqual("""{"isOk": true, "message": "Ok", "data": "a data piece"}""", str(r))
        r2 = ReportJson.fromResultWithErrorReport(Ok([1, 2, 3]))
        self.assertEqual("""{"isOk": true, "message": "Ok", "data": "[1, 2, 3]"}""", str(r2))
        r3 = ReportJson.fromResultWithErrorReport(Ok(A()))
        self.assertEqual("""{"isOk": true, "message": "Ok", "data": "{\\\"x\\\": 123, \\\"y\\\": \\\"abc qqqq\\\"}"}""",
                         str(r3))

        r4 = ReportJson.fromResultWithErrorReport(Ok(B()))
        self.assertEqual("""{"isOk": true, "message": "Ok", "data": "{\\\"x\\\": 123, \\\"y\\\": \\\"abc qqqq\\\"}"}""",
                         str(r4))

    def test_fromErrResult(self):
        r3 = ReportJson.fromResultWithErrorReport(Err(
            ErrorReport(
                header=ErrorHeader("Code1", "Error message"),
                data=A()
            )
        ))
        self.assertEqual(
            """{"isOk": false, "message": "Code1: Error message", "data": "{\\\"x\\\": 123, \\\"y\\\": \\\"abc qqqq\\\"}"}""",
            str(r3))

        r4 = ReportJson.fromResultWithErrorReport(Err(
            ErrorReport(
                header=ErrorHeader("Code1", "Error message"),
                data=B()
            )
        ))
        self.assertEqual(
            """{"isOk": false, "message": "Code1: Error message", "data": "{\\\"x\\\": 123, \\\"y\\\": \\\"abc qqqq\\\"}"}""",
            str(r4))


if __name__ == '__main__':
    unittest.main()
