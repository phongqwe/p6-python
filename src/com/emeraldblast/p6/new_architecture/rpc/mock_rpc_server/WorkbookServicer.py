from concurrent import futures

import grpc

from com.emeraldblast.p6.proto.service.workbook import WorkbookService_pb2_grpc
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2_grpc import WorkbookServiceServicer
from google.protobuf import wrappers_pb2 as wrappers


class WorkbookServicerImp(WorkbookServiceServicer):
    def sheetCount(self, request, context):
        return wrappers.Int64Value(123)



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    WorkbookService_pb2_grpc.add_WorkbookServiceServicer_to_server(
        WorkbookServicerImp(),server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
