# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/qxdzbc/p6/proto/rpc/cell/CellServiceProtos.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.qxdzbc.p6.proto import CommonProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_CommonProtos__pb2
from com.qxdzbc.p6.proto import DocProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_DocProtos__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4com/qxdzbc/p6/proto/rpc/cell/CellServiceProtos.proto\x12\x1c\x63om.qxdzbc.p6.proto.rpc.cell\x1a&com/qxdzbc/p6/proto/CommonProtos.proto\x1a#com/qxdzbc/p6/proto/DocProtos.proto\"B\n\x0eGetCellRequest\x12\x30\n\x06\x63\x65llId\x18\x01 \x01(\x0b\x32 .com.qxdzbc.p6.proto.CellIdProto\"$\n\x0fGetCellResponse\x12\x11\n\tcellValue\x18\x01 \x01(\tb\x06proto3')



_GETCELLREQUEST = DESCRIPTOR.message_types_by_name['GetCellRequest']
_GETCELLRESPONSE = DESCRIPTOR.message_types_by_name['GetCellResponse']
GetCellRequest = _reflection.GeneratedProtocolMessageType('GetCellRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCELLREQUEST,
  '__module__' : 'com.qxdzbc.p6.proto.rpc.cell.CellServiceProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.rpc.cell.GetCellRequest)
  })
_sym_db.RegisterMessage(GetCellRequest)

GetCellResponse = _reflection.GeneratedProtocolMessageType('GetCellResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCELLRESPONSE,
  '__module__' : 'com.qxdzbc.p6.proto.rpc.cell.CellServiceProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.rpc.cell.GetCellResponse)
  })
_sym_db.RegisterMessage(GetCellResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETCELLREQUEST._serialized_start=163
  _GETCELLREQUEST._serialized_end=229
  _GETCELLRESPONSE._serialized_start=231
  _GETCELLRESPONSE._serialized_end=267
# @@protoc_insertion_point(module_scope)
