# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/qxdzbc/p6/proto/rpc/cell/service/CellService.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.qxdzbc.p6.proto.rpc.cell import CellServiceProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_rpc_dot_cell_dot_CellServiceProtos__pb2
from com.qxdzbc.p6.proto import CommonProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2
from com.qxdzbc.p6.proto import CellProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_CellProtos__pb2
from com.qxdzbc.p6.proto import DocProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6com/qxdzbc/p6/proto/rpc/cell/service/CellService.proto\x12$com.qxdzbc.p6.proto.rpc.cell.service\x1a\x34\x63om/qxdzbc/p6/proto/rpc/cell/CellServiceProtos.proto\x1a&com/qxdzbc/p6/proto/CommonProtos.proto\x1a$com/qxdzbc/p6/proto/CellProtos.proto\x1a#com/qxdzbc/p6/proto/DocProtos.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1bgoogle/protobuf/empty.proto2\xe2\x03\n\x0b\x43\x65llService\x12W\n\x0fgetDisplayValue\x12 .com.qxdzbc.p6.proto.CellIdProto\x1a .com.qxdzbc.p6.proto.StrMsgProto\"\x00\x12R\n\ngetFormula\x12 .com.qxdzbc.p6.proto.CellIdProto\x1a .com.qxdzbc.p6.proto.StrMsgProto\"\x00\x12W\n\x0cgetCellValue\x12 .com.qxdzbc.p6.proto.CellIdProto\x1a#.com.qxdzbc.p6.proto.CellValueProto\"\x00\x12[\n\x0egetCellContent\x12 .com.qxdzbc.p6.proto.CellIdProto\x1a%.com.qxdzbc.p6.proto.CellContentProto\"\x00\x12p\n\x08\x63opyFrom\x12\x32.com.qxdzbc.p6.proto.rpc.cell.CopyCellRequestProto\x1a..com.qxdzbc.p6.proto.SingleSignalResponseProto\"\x00\x62\x06proto3')



_CELLSERVICE = DESCRIPTOR.services_by_name['CellService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CELLSERVICE._serialized_start=327
  _CELLSERVICE._serialized_end=809
# @@protoc_insertion_point(module_scope)
