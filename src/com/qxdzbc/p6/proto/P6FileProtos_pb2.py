# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/qxdzbc/p6/proto/P6FileProtos.proto
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
from com.qxdzbc.p6.proto import ScriptProtos_pb2 as com_dot_qxdzbc_dot_p6_dot_proto_dot_ScriptProtos__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&com/qxdzbc/p6/proto/P6FileProtos.proto\x12\x13\x63om.qxdzbc.p6.proto\x1a&com/qxdzbc/p6/proto/CommonProtos.proto\x1a#com/qxdzbc/p6/proto/DocProtos.proto\x1a&com/qxdzbc/p6/proto/ScriptProtos.proto\"#\n\x13P6FileMetaInfoProto\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\x02\"\x82\x01\n\x12P6FileContentProto\x12\x36\n\x04meta\x18\x01 \x01(\x0b\x32(.com.qxdzbc.p6.proto.P6FileMetaInfoProto\x12\x34\n\x08workbook\x18\x02 \x01(\x0b\x32\".com.qxdzbc.p6.proto.WorkbookProto\"/\n\x0bP6FileProto\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\x62\x06proto3')



_P6FILEMETAINFOPROTO = DESCRIPTOR.message_types_by_name['P6FileMetaInfoProto']
_P6FILECONTENTPROTO = DESCRIPTOR.message_types_by_name['P6FileContentProto']
_P6FILEPROTO = DESCRIPTOR.message_types_by_name['P6FileProto']
P6FileMetaInfoProto = _reflection.GeneratedProtocolMessageType('P6FileMetaInfoProto', (_message.Message,), {
  'DESCRIPTOR' : _P6FILEMETAINFOPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.P6FileProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.P6FileMetaInfoProto)
  })
_sym_db.RegisterMessage(P6FileMetaInfoProto)

P6FileContentProto = _reflection.GeneratedProtocolMessageType('P6FileContentProto', (_message.Message,), {
  'DESCRIPTOR' : _P6FILECONTENTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.P6FileProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.P6FileContentProto)
  })
_sym_db.RegisterMessage(P6FileContentProto)

P6FileProto = _reflection.GeneratedProtocolMessageType('P6FileProto', (_message.Message,), {
  'DESCRIPTOR' : _P6FILEPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.P6FileProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.P6FileProto)
  })
_sym_db.RegisterMessage(P6FileProto)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _P6FILEMETAINFOPROTO._serialized_start=180
  _P6FILEMETAINFOPROTO._serialized_end=215
  _P6FILECONTENTPROTO._serialized_start=218
  _P6FILECONTENTPROTO._serialized_end=348
  _P6FILEPROTO._serialized_start=350
  _P6FILEPROTO._serialized_end=397
# @@protoc_insertion_point(module_scope)