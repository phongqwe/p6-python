from pathlib import Path


class A:
    def __init__(self):
        pass
    def z(self):
        return 100
if __name__ == "__main__":
    p =Path(Path("cc/dd/ee/abc.txt"))
    print(p.name)
