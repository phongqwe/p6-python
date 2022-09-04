from com.qxdzbc.p6.document_structure.util.CommonError import CommonErrors
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.new_architecture.rpc.RpcErrors import RpcErrors


class RpcUtils:
    _serverDownReport = RpcErrors.RpcServerIsDown \
        .report("Can't make rpc request because rpc server is down.")
    _serverDownException = _serverDownReport.toException()

    @staticmethod
    def onServiceOkRs(rpcStub, f):
        if rpcStub is not None:
            try:
                return f()
            except Exception as e:
                return Err(CommonErrors.ExceptionErrorReport.report(e))
        else:
            return RpcUtils._serverDownReport

    @staticmethod
    def onServiceOk(rpcStub, f):
        if rpcStub is not None:
            return f()
        else:
            raise RpcUtils._serverDownException
