# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from com.emeraldblast.p6.proto import CommonProtos_pb2 as com_dot_emeraldblast_dot_p6_dot_proto_dot_CommonProtos__pb2
from com.emeraldblast.p6.proto import DocProtos_pb2 as com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2
from com.emeraldblast.p6.proto.service.workbook import GetActiveWorksheetResponseProto_pb2 as com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_GetActiveWorksheetResponseProto__pb2
from com.emeraldblast.p6.proto.service.workbook import GetAllWorksheets_pb2 as com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_GetAllWorksheets__pb2
from com.emeraldblast.p6.proto.service.workbook import SetActiveWorksheetRequestProto_pb2 as com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_SetActiveWorksheetRequestProto__pb2
from com.emeraldblast.p6.proto.service.workbook import SetWbName_pb2 as com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_SetWbName__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


class WorkbookServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.sheetCount = channel.unary_unary(
                '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/sheetCount',
                request_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_wrappers__pb2.Int64Value.FromString,
                )
        self.setWbName = channel.unary_unary(
                '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/setWbName',
                request_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_SetWbName__pb2.SetWbNameRequestProto.SerializeToString,
                response_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
                )
        self.getAllWorksheets = channel.unary_unary(
                '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/getAllWorksheets',
                request_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
                response_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_GetAllWorksheets__pb2.GetAllWorksheetsResponseProto.FromString,
                )
        self.setActiveWorksheetRs = channel.unary_unary(
                '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/setActiveWorksheetRs',
                request_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_SetActiveWorksheetRequestProto__pb2.SetActiveWorksheetRequestProto.SerializeToString,
                response_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
                )
        self.getActiveWorksheet = channel.unary_unary(
                '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/getActiveWorksheet',
                request_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
                response_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_GetActiveWorksheetResponseProto__pb2.GetActiveWorksheetResponseProto.FromString,
                )


class WorkbookServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def sheetCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setWbName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAllWorksheets(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setActiveWorksheetRs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getActiveWorksheet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkbookServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'sheetCount': grpc.unary_unary_rpc_method_handler(
                    servicer.sheetCount,
                    request_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.FromString,
                    response_serializer=google_dot_protobuf_dot_wrappers__pb2.Int64Value.SerializeToString,
            ),
            'setWbName': grpc.unary_unary_rpc_method_handler(
                    servicer.setWbName,
                    request_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_SetWbName__pb2.SetWbNameRequestProto.FromString,
                    response_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.SerializeToString,
            ),
            'getAllWorksheets': grpc.unary_unary_rpc_method_handler(
                    servicer.getAllWorksheets,
                    request_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.FromString,
                    response_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_GetAllWorksheets__pb2.GetAllWorksheetsResponseProto.SerializeToString,
            ),
            'setActiveWorksheetRs': grpc.unary_unary_rpc_method_handler(
                    servicer.setActiveWorksheetRs,
                    request_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_SetActiveWorksheetRequestProto__pb2.SetActiveWorksheetRequestProto.FromString,
                    response_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.SerializeToString,
            ),
            'getActiveWorksheet': grpc.unary_unary_rpc_method_handler(
                    servicer.getActiveWorksheet,
                    request_deserializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.FromString,
                    response_serializer=com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_GetActiveWorksheetResponseProto__pb2.GetActiveWorksheetResponseProto.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.emeraldblast.p6.proto.service.workbook.WorkbookService', rpc_method_handlers)
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
        return grpc.experimental.unary_unary(request, target, '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/sheetCount',
            com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
            google_dot_protobuf_dot_wrappers__pb2.Int64Value.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def setWbName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/setWbName',
            com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_SetWbName__pb2.SetWbNameRequestProto.SerializeToString,
            com_dot_emeraldblast_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/getAllWorksheets',
            com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
            com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_GetAllWorksheets__pb2.GetAllWorksheetsResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def setActiveWorksheetRs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/setActiveWorksheetRs',
            com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_SetActiveWorksheetRequestProto__pb2.SetActiveWorksheetRequestProto.SerializeToString,
            com_dot_emeraldblast_dot_p6_dot_proto_dot_CommonProtos__pb2.SingleSignalResponseProto.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/com.emeraldblast.p6.proto.service.workbook.WorkbookService/getActiveWorksheet',
            com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2.WorkbookKeyProto.SerializeToString,
            com_dot_emeraldblast_dot_p6_dot_proto_dot_service_dot_workbook_dot_GetActiveWorksheetResponseProto__pb2.GetActiveWorksheetResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
