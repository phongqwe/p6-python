import unittest

from bicp_document_structure.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem


class AlphabetBaseNumberSystem_test(unittest.TestCase):

    def test_z(self):
        data = {
            "A":1,
            "B":2,
            "C":3,
            "D":4,
            "Z":26,
            "AA":27,
            "AZ":52,
            "BA":53,
            "AAA":703,
            "AW":49,
            "SJ":504,
            "AII":919,
            "AEO":821,
            "ABO":743,
        }
        for k,v in data.items():
            self.assertEqual(v,AlphabetBaseNumberSystem.translate(k))