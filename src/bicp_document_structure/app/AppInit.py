from bicp_document_structure.app.App import App
from bicp_document_structure.app.SingleBookApp import SingleBookApp


class AppInit:
    __appInstance = None
    @staticmethod
    def getApp()->App:
        if AppInit.__appInstance is not None:
            return AppInit.__appInstance
        else:
            AppInit.__appInstance = SingleBookApp()