# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from com.qxdzbc.p6.proto import CommonProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2
from com.qxdzbc.p6.proto import DocProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2
from com.qxdzbc.p6.proto import WorksheetProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2
from com.qxdzbc.p6.proto.rpc.workbook import WorkbooKServiceProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


class WorkbookServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.sheetCount = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/sheetCount',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_wrappers__pb2.Int64Value.FromString,
                )
        self.setWbKey = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/setWbKey',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.SetWbKeyRequestProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
                )
        self.getAllWorksheets = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/getAllWorksheets',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetAllWorksheetsResponseProto.FromString,
                )
        self.setActiveWorksheet = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/setActiveWorksheet',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
                )
        self.getActiveWorksheet = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/getActiveWorksheet',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetWorksheetResponseProto.FromString,
                )
        self.getWorksheet = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/getWorksheet',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetWorksheetResponseProto.FromString,
                )
        self.createNewWorksheet = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/createNewWorksheet',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.CreateNewWorksheetRequestProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.WorksheetWithErrorReportMsgProto.FromString,
                )
        self.deleteWorksheet = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/deleteWorksheet',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
                )
        self.addWorksheet = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/addWorksheet',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.AddWorksheetRequestProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
                )
        self.renameWorksheet = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/renameWorksheet',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.RenameWorksheetRequestProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
                )


class WorkbookServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def sheetCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setWbKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAllWorksheets(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setActiveWorksheet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getActiveWorksheet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getWorksheet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createNewWorksheet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteWorksheet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addWorksheet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def renameWorksheet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkbookServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'sheetCount': grpc.unary_unary_rpc_method_handler(
                    servicer.sheetCount,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.FromString,
                    response_serializer=google_dot_protobuf_dot_wrappers__pb2.Int64Value.SerializeToString,
            ),
            'setWbKey': grpc.unary_unary_rpc_method_handler(
                    servicer.setWbKey,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.SetWbKeyRequestProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.SerializeToString,
            ),
            'getAllWorksheets': grpc.unary_unary_rpc_method_handler(
                    servicer.getAllWorksheets,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetAllWorksheetsResponseProto.SerializeToString,
            ),
            'setActiveWorksheet': grpc.unary_unary_rpc_method_handler(
                    servicer.setActiveWorksheet,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.SerializeToString,
            ),
            'getActiveWorksheet': grpc.unary_unary_rpc_method_handler(
                    servicer.getActiveWorksheet,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetWorksheetResponseProto.SerializeToString,
            ),
            'getWorksheet': grpc.unary_unary_rpc_method_handler(
                    servicer.getWorksheet,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetWorksheetResponseProto.SerializeToString,
            ),
            'createNewWorksheet': grpc.unary_unary_rpc_method_handler(
                    servicer.createNewWorksheet,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.CreateNewWorksheetRequestProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.WorksheetWithErrorReportMsgProto.SerializeToString,
            ),
            'deleteWorksheet': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteWorksheet,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.SerializeToString,
            ),
            'addWorksheet': grpc.unary_unary_rpc_method_handler(
                    servicer.addWorksheet,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.AddWorksheetRequestProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.SerializeToString,
            ),
            'renameWorksheet': grpc.unary_unary_rpc_method_handler(
                    servicer.renameWorksheet,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.RenameWorksheetRequestProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkbookService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def sheetCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/sheetCount',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
            google_dot_protobuf_dot_wrappers__pb2.Int64Value.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def setWbKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/setWbKey',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.SetWbKeyRequestProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getAllWorksheets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/getAllWorksheets',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetAllWorksheetsResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def setActiveWorksheet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/setActiveWorksheet',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getActiveWorksheet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/getActiveWorksheet',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetWorksheetResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getWorksheet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/getWorksheet',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.GetWorksheetResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def createNewWorksheet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/createNewWorksheet',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.CreateNewWorksheetRequestProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.WorksheetWithErrorReportMsgProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteWorksheet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/deleteWorksheet',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_WorksheetProtos__pb2.WorksheetIdProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addWorksheet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/addWorksheet',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.AddWorksheetRequestProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def renameWorksheet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService/renameWorksheet',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_workbook_dot_WorkbooKServiceProtos__pb2.RenameWorksheetRequestProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
