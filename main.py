from com.qxdzbc.p6.new_architecture.communication import P6Events


def main():
    for e in P6Events.Worksheet.allEvents():
        print(e.name)

if __name__ == "__main__":
    main()
