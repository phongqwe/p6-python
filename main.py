import json


class A:
    def __init__(self):
        self.x=1
        self.y = 333
    def zzz(self):
        return 1000

if __name__ == "__main__":
    print(json.dumps(A().__dict__))
