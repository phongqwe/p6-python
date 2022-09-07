# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/qxdzbc/p6/proto/CellProtos.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$com/qxdzbc/p6/proto/CellProtos.proto\x12\x13\x63om.qxdzbc.p6.proto\x1a&com/qxdzbc/p6/proto/CommonProtos.proto\x1a#com/qxdzbc/p6/proto/DocProtos.proto\"\xc7\x01\n\x16\x43\x65llUpdateRequestProto\x12:\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x02 \x01(\t\x12:\n\x0b\x63\x65llAddress\x18\x03 \x01(\x0b\x32%.com.qxdzbc.p6.proto.CellAddressProto\x12\r\n\x05value\x18\x04 \x01(\t\x12\x0f\n\x07\x66ormula\x18\x05 \x01(\t\":\n\x16\x43\x65llUpdateContentProto\x12\x0f\n\x07\x66ormula\x18\x01 \x01(\t\x12\x0f\n\x07literal\x18\x02 \x01(\t\"\x90\x01\n\x14\x43\x65llUpdateEntryProto\x12:\n\x0b\x63\x65llAddress\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.CellAddressProto\x12<\n\x07\x63ontent\x18\x02 \x01(\x0b\x32+.com.qxdzbc.p6.proto.CellUpdateContentProto\"\xaf\x01\n\x1b\x43\x65llMultiUpdateRequestProto\x12:\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x02 \x01(\t\x12=\n\ncellUpdate\x18\x03 \x03(\x0b\x32).com.qxdzbc.p6.proto.CellUpdateEntryProto\"l\n\x10\x43\x65llContentProto\x12\x36\n\tcellValue\x18\x01 \x01(\x0b\x32#.com.qxdzbc.p6.proto.CellValueProto\x12\x14\n\x07\x66ormula\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\n\n\x08_formulab\x06proto3')



_CELLUPDATEREQUESTPROTO = DESCRIPTOR.message_types_by_name['CellUpdateRequestProto']
_CELLUPDATECONTENTPROTO = DESCRIPTOR.message_types_by_name['CellUpdateContentProto']
_CELLUPDATEENTRYPROTO = DESCRIPTOR.message_types_by_name['CellUpdateEntryProto']
_CELLMULTIUPDATEREQUESTPROTO = DESCRIPTOR.message_types_by_name['CellMultiUpdateRequestProto']
_CELLCONTENTPROTO = DESCRIPTOR.message_types_by_name['CellContentProto']
CellUpdateRequestProto = _reflection.GeneratedProtocolMessageType('CellUpdateRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLUPDATEREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.CellUpdateRequestProto)
  })
_sym_db.RegisterMessage(CellUpdateRequestProto)

CellUpdateContentProto = _reflection.GeneratedProtocolMessageType('CellUpdateContentProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLUPDATECONTENTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.CellUpdateContentProto)
  })
_sym_db.RegisterMessage(CellUpdateContentProto)

CellUpdateEntryProto = _reflection.GeneratedProtocolMessageType('CellUpdateEntryProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLUPDATEENTRYPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.CellUpdateEntryProto)
  })
_sym_db.RegisterMessage(CellUpdateEntryProto)

CellMultiUpdateRequestProto = _reflection.GeneratedProtocolMessageType('CellMultiUpdateRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLMULTIUPDATEREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.CellMultiUpdateRequestProto)
  })
_sym_db.RegisterMessage(CellMultiUpdateRequestProto)

CellContentProto = _reflection.GeneratedProtocolMessageType('CellContentProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLCONTENTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.CellContentProto)
  })
_sym_db.RegisterMessage(CellContentProto)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CELLUPDATEREQUESTPROTO._serialized_start=139
  _CELLUPDATEREQUESTPROTO._serialized_end=338
  _CELLUPDATECONTENTPROTO._serialized_start=340
  _CELLUPDATECONTENTPROTO._serialized_end=398
  _CELLUPDATEENTRYPROTO._serialized_start=401
  _CELLUPDATEENTRYPROTO._serialized_end=545
  _CELLMULTIUPDATEREQUESTPROTO._serialized_start=548
  _CELLMULTIUPDATEREQUESTPROTO._serialized_end=723
  _CELLCONTENTPROTO._serialized_start=725
  _CELLCONTENTPROTO._serialized_end=833
# @@protoc_insertion_point(module_scope)