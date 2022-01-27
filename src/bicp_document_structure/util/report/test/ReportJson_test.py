import unittest

from bicp_document_structure.util.report.ReportJson import ReportJson


class ReportJson_test(unittest.TestCase):
    def test_toJson(self):
        r = ReportJson(True,"a message",{
            "a":1,
            "b":"b2"
        })
        self.assertEqual("""{"isOk": true, "message": "a message", "data": {"a": 1, "b": "b2"}}""",str(r))


if __name__ == '__main__':
    unittest.main()
