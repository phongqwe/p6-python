from com.qxdzbc.p6.document_structure.communication.event.P6Events import P6Events
import inspect

def main():
    for e in P6Events.Worksheet.allEvents():
        print(e.name)

if __name__ == "__main__":
    main()
