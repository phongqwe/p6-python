from pathlib import Path


def writeTestLog(msg:str):
    path = Path("/home/abc/MyTemp/testLog.txt")
    f = open(path,"a")
    f.write(msg+"\n")
    f.close()