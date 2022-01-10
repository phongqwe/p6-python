import string

from bicp_document_structure.util.Util import typeCheck


class AlphabetBaseNumberSystem:
    """
    translate col latter to index
    A -> 1
    B -> 2
    ...
    Z -> 26
    AA -> 27
    """

    __alphabet = list(string.ascii_uppercase)
    __scale = len(__alphabet)

    @staticmethod
    def toDecimal(abcNumber: str) -> int:
        typeCheck(abcNumber,"abcNumber",str)
        rt = 0
        # loop from the last char to the first char
        for i, c in enumerate(reversed(abcNumber)):
            weight = AlphabetBaseNumberSystem.__scale ** i
            # charIndex is index of the c char in the alphabet + 1
            charIndex = AlphabetBaseNumberSystem.__alphabet.index(c.upper()) + 1
            n = weight * charIndex
            rt += n
        return rt

    @staticmethod
    def fromDecimal(number:int)->str:
        scale = 26
        if number <= scale:
            return string.ascii_uppercase[number-1]

        rt = ""
        iterNum = number
        prevZero = False
        while True:
            if iterNum == 0:
                break
            result = int(iterNum/scale)
            remainder = iterNum % scale
            charIndex = -1
            if remainder != 0:
                if prevZero:
                    charIndex = int(remainder-2)
                else:
                    charIndex = int(remainder-1)
            else:
                charIndex = scale-1
            prevZero = (remainder==0)
            rt = rt + string.ascii_uppercase[charIndex]
            iterNum =result
        return rt[::-1] # reversed