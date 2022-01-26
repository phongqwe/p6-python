class A:
    def __init__(self):
        pass
    def z(self):
        return 100
if __name__ == "__main__":
    d = {
        1:"1v",
        2:"2v"
    }
    l = list(d.values())
    d.clear()
    print(l)
