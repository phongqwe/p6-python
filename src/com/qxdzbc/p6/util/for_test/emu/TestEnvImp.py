from com.qxdzbc.p6.workbook import WorkbookImp


class TestEnvImp:
    """
    How to use:
        testEnv = TestEnvImp()
        testEnv.startApp()

        use sendRequestToEventServer() to send request to event server
        use self.notifListener.addReactor() to add notification reactor

        This test env emulate a real app which consist of:
            2 workbooks, each workbook consist of 2 sheets. All wb and ws can emit events
            1 event server
            1 notification listener
    """

    def __init__(self):
        self._app = None

    @staticmethod
    def sampleWb(name):
        wb = WorkbookImp(name)
        s1 = wb.createNewWorksheet("Sheet1")
        s2 = wb.createNewWorksheet("Sheet2")
        s1.getCell((1, 1)).value = 11
        s1.getCell((2, 2)).value = 22
        s1.getCell((3, 3)).value = 33
        s2.getCell((1, 1)).value = 211
        s2.getCell((2, 2)).value = 222
        s2.getCell((3, 3)).value = 233
        return wb

    def startEnv(self):
        # these import will be put in local
        from com.qxdzbc.p6.app import setIPythonGlobals
        from com.qxdzbc.p6.app import startApp, getApp

        local = locals()
        globals()

        setIPythonGlobals({**local, **globals()})
        startApp()
        self._app = getApp()

        b1 = getApp().createNewWorkbook("Book1")
        b1.createNewWorksheet("Sheet1")
        b1.createNewWorksheet("Sheet2")

        b2 = getApp().createNewWorkbook("Book2")
        b2.createNewWorksheet("Sheet1")
        b2.createNewWorksheet("Sheet2")


    def stopAll(self):
        stopApp()

    @property
    def app(self)-> App:
        return self._app
