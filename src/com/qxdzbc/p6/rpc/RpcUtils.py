from typing import Any

from com.qxdzbc.p6.util.CommonError import CommonErrors
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.rpc.RpcErrors import RpcErrors


class RpcUtils:
    _serverDownReport = RpcErrors.RpcServerIsDown \
        .report("Can't make rpc request because rpc server is down.")
    _serverDownException = _serverDownReport.toException()

    @staticmethod
    def onServiceOkRs(rpcStub, f)->Result[Any,ErrorReport]:
        """
        a catch-all block
        :param rpcStub:
        :param f:
        :return:
        """
        if rpcStub is not None:
            try:
                return f()
            except Exception as e:
                return Err(CommonErrors.ExceptionErrorReport.report(e))
        else:
            return RpcUtils._serverDownReport

    @staticmethod
    def onServiceOkOrRaise(rpcStub, f):
        if rpcStub is not None:
            return f()
        else:
            raise RpcUtils._serverDownException

    @staticmethod
    def onServiceOkOrNone(rpcStub, f):
        if rpcStub is not None:
            return f()
        else:
            return None
