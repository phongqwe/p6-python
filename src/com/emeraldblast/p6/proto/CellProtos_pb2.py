# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/emeraldblast/p6/proto/CellProtos.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.emeraldblast.p6.proto import CommonProtos_pb2 as com_dot_emeraldblast_dot_p6_dot_proto_dot_CommonProtos__pb2
from com.emeraldblast.p6.proto import DocProtos_pb2 as com_dot_emeraldblast_dot_p6_dot_proto_dot_DocProtos__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*com/emeraldblast/p6/proto/CellProtos.proto\x12\x19\x63om.emeraldblast.p6.proto\x1a,com/emeraldblast/p6/proto/CommonProtos.proto\x1a)com/emeraldblast/p6/proto/DocProtos.proto\"\xd3\x01\n\x16\x43\x65llUpdateRequestProto\x12@\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32+.com.emeraldblast.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x02 \x01(\t\x12@\n\x0b\x63\x65llAddress\x18\x03 \x01(\x0b\x32+.com.emeraldblast.p6.proto.CellAddressProto\x12\r\n\x05value\x18\x04 \x01(\t\x12\x0f\n\x07\x66ormula\x18\x05 \x01(\t\"\xf3\x01\n\x1d\x43\x65llUpdateCommonResponseProto\x12@\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32+.com.emeraldblast.p6.proto.WorkbookKeyProto\x12=\n\x0bnewWorkbook\x18\x02 \x01(\x0b\x32(.com.emeraldblast.p6.proto.WorkbookProto\x12\x0f\n\x07isError\x18\x03 \x01(\x08\x12@\n\x0b\x65rrorReport\x18\x04 \x01(\x0b\x32+.com.emeraldblast.p6.proto.ErrorReportProto\":\n\x16\x43\x65llUpdateContentProto\x12\x0f\n\x07\x66ormula\x18\x01 \x01(\t\x12\x0f\n\x07literal\x18\x02 \x01(\t\"\xa0\x01\n\x15SingleCellUpdateProto\x12@\n\x0b\x63\x65llAddress\x18\x01 \x01(\x0b\x32+.com.emeraldblast.p6.proto.CellAddressProto\x12\x45\n\ncellUpdate\x18\x02 \x01(\x0b\x32\x31.com.emeraldblast.p6.proto.CellUpdateContentProto\"\xbc\x01\n\x1b\x43\x65llMultiUpdateRequestProto\x12@\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32+.com.emeraldblast.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x02 \x01(\t\x12\x44\n\ncellUpdate\x18\x03 \x03(\x0b\x32\x30.com.emeraldblast.p6.proto.SingleCellUpdateProtob\x06proto3')



_CELLUPDATEREQUESTPROTO = DESCRIPTOR.message_types_by_name['CellUpdateRequestProto']
_CELLUPDATECOMMONRESPONSEPROTO = DESCRIPTOR.message_types_by_name['CellUpdateCommonResponseProto']
_CELLUPDATECONTENTPROTO = DESCRIPTOR.message_types_by_name['CellUpdateContentProto']
_SINGLECELLUPDATEPROTO = DESCRIPTOR.message_types_by_name['SingleCellUpdateProto']
_CELLMULTIUPDATEREQUESTPROTO = DESCRIPTOR.message_types_by_name['CellMultiUpdateRequestProto']
CellUpdateRequestProto = _reflection.GeneratedProtocolMessageType('CellUpdateRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLUPDATEREQUESTPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.CellUpdateRequestProto)
  })
_sym_db.RegisterMessage(CellUpdateRequestProto)

CellUpdateCommonResponseProto = _reflection.GeneratedProtocolMessageType('CellUpdateCommonResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLUPDATECOMMONRESPONSEPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.CellUpdateCommonResponseProto)
  })
_sym_db.RegisterMessage(CellUpdateCommonResponseProto)

CellUpdateContentProto = _reflection.GeneratedProtocolMessageType('CellUpdateContentProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLUPDATECONTENTPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.CellUpdateContentProto)
  })
_sym_db.RegisterMessage(CellUpdateContentProto)

SingleCellUpdateProto = _reflection.GeneratedProtocolMessageType('SingleCellUpdateProto', (_message.Message,), {
  'DESCRIPTOR' : _SINGLECELLUPDATEPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.SingleCellUpdateProto)
  })
_sym_db.RegisterMessage(SingleCellUpdateProto)

CellMultiUpdateRequestProto = _reflection.GeneratedProtocolMessageType('CellMultiUpdateRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _CELLMULTIUPDATEREQUESTPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.CellProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.CellMultiUpdateRequestProto)
  })
_sym_db.RegisterMessage(CellMultiUpdateRequestProto)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CELLUPDATEREQUESTPROTO._serialized_start=163
  _CELLUPDATEREQUESTPROTO._serialized_end=374
  _CELLUPDATECOMMONRESPONSEPROTO._serialized_start=377
  _CELLUPDATECOMMONRESPONSEPROTO._serialized_end=620
  _CELLUPDATECONTENTPROTO._serialized_start=622
  _CELLUPDATECONTENTPROTO._serialized_end=680
  _SINGLECELLUPDATEPROTO._serialized_start=683
  _SINGLECELLUPDATEPROTO._serialized_end=843
  _CELLMULTIUPDATEREQUESTPROTO._serialized_start=846
  _CELLMULTIUPDATEREQUESTPROTO._serialized_end=1034
# @@protoc_insertion_point(module_scope)
