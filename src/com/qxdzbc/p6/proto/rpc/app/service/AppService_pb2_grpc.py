# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from com.qxdzbc.p6.proto.rpc.app import AppServiceProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_app_dot_AppServiceProtos__pb2


class AppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getWorkbook = channel.unary_unary(
                '/com.qxdzbc.p6.proto.rpc.app.service.AppService/getWorkbook',
                request_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_app_dot_AppServiceProtos__pb2.GetWorkbookRequestProto.SerializeToString,
                response_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_app_dot_AppServiceProtos__pb2.WorkbookKeyWithErrorResponseProto.FromString,
                )


class AppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getWorkbook(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getWorkbook': grpc.unary_unary_rpc_method_handler(
                    servicer.getWorkbook,
                    request_deserializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_app_dot_AppServiceProtos__pb2.GetWorkbookRequestProto.FromString,
                    response_serializer=com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_app_dot_AppServiceProtos__pb2.WorkbookKeyWithErrorResponseProto.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.qxdzbc.p6.proto.rpc.app.service.AppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getWorkbook(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.qxdzbc.p6.proto.rpc.app.service.AppService/getWorkbook',
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_app_dot_AppServiceProtos__pb2.GetWorkbookRequestProto.SerializeToString,
            com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_app_dot_AppServiceProtos__pb2.WorkbookKeyWithErrorResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
