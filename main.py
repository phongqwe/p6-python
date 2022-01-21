class A:
    def __init__(self):
        pass
    def z(self):
        return 100
if __name__ == "__main__":
    d1 = {1: 2, 3: 4}
    d2 = {5: 6, 7: 9}
    d3 = {10: 8, 13: 22}
    all = {}
    all.update(d1)
    all.update(d2)
    print(all)