# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/emeraldblast/p6/proto/WorksheetProtos.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/com/emeraldblast/p6/proto/WorksheetProtos.proto\x12\x19\x63om.emeraldblast.p6.proto\x1a,com/emeraldblast/p6/proto/CommonProtos.proto\x1a)com/emeraldblast/p6/proto/DocProtos.proto\"\x81\x01\n\x1bRenameWorksheetRequestProto\x12@\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32+.com.emeraldblast.p6.proto.WorkbookKeyProto\x12\x0f\n\x07oldName\x18\x02 \x01(\t\x12\x0f\n\x07newName\x18\x03 \x01(\t\"\xd5\x01\n\x1cRenameWorksheetResponseProto\x12@\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32+.com.emeraldblast.p6.proto.WorkbookKeyProto\x12\x0f\n\x07oldName\x18\x02 \x01(\t\x12\x0f\n\x07newName\x18\x03 \x01(\t\x12\x0f\n\x07isError\x18\x04 \x01(\x08\x12@\n\x0b\x65rrorReport\x18\x05 \x01(\x0b\x32+.com.emeraldblast.p6.proto.ErrorReportProto\"\xb3\x01\n\x16\x44\x65leteCellRequestProto\x12@\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32+.com.emeraldblast.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x02 \x01(\t\x12@\n\x0b\x63\x65llAddress\x18\x03 \x01(\x0b\x32+.com.emeraldblast.p6.proto.CellAddressProto\"\xc6\x02\n\x17\x44\x65leteCellResponseProto\x12@\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32+.com.emeraldblast.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x02 \x01(\t\x12@\n\x0b\x63\x65llAddress\x18\x03 \x01(\x0b\x32+.com.emeraldblast.p6.proto.CellAddressProto\x12=\n\x0bnewWorkbook\x18\x04 \x01(\x0b\x32(.com.emeraldblast.p6.proto.WorkbookProto\x12\x0f\n\x07isError\x18\x05 \x01(\x08\x12@\n\x0b\x65rrorReport\x18\x06 \x01(\x0b\x32+.com.emeraldblast.p6.proto.ErrorReportProto\"\xea\x01\n\x17\x44\x65leteMultiRequestProto\x12;\n\x05range\x18\x01 \x03(\x0b\x32,.com.emeraldblast.p6.proto.RangeAddressProto\x12\x39\n\x04\x63\x65ll\x18\x02 \x03(\x0b\x32+.com.emeraldblast.p6.proto.CellAddressProto\x12@\n\x0bworkbookKey\x18\x03 \x01(\x0b\x32+.com.emeraldblast.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x04 \x01(\tb\x06proto3')



_RENAMEWORKSHEETREQUESTPROTO = DESCRIPTOR.message_types_by_name['RenameWorksheetRequestProto']
_RENAMEWORKSHEETRESPONSEPROTO = DESCRIPTOR.message_types_by_name['RenameWorksheetResponseProto']
_DELETECELLREQUESTPROTO = DESCRIPTOR.message_types_by_name['DeleteCellRequestProto']
_DELETECELLRESPONSEPROTO = DESCRIPTOR.message_types_by_name['DeleteCellResponseProto']
_DELETEMULTIREQUESTPROTO = DESCRIPTOR.message_types_by_name['DeleteMultiRequestProto']
RenameWorksheetRequestProto = _reflection.GeneratedProtocolMessageType('RenameWorksheetRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _RENAMEWORKSHEETREQUESTPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.WorksheetProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.RenameWorksheetRequestProto)
  })
_sym_db.RegisterMessage(RenameWorksheetRequestProto)

RenameWorksheetResponseProto = _reflection.GeneratedProtocolMessageType('RenameWorksheetResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _RENAMEWORKSHEETRESPONSEPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.WorksheetProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.RenameWorksheetResponseProto)
  })
_sym_db.RegisterMessage(RenameWorksheetResponseProto)

DeleteCellRequestProto = _reflection.GeneratedProtocolMessageType('DeleteCellRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _DELETECELLREQUESTPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.WorksheetProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.DeleteCellRequestProto)
  })
_sym_db.RegisterMessage(DeleteCellRequestProto)

DeleteCellResponseProto = _reflection.GeneratedProtocolMessageType('DeleteCellResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _DELETECELLRESPONSEPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.WorksheetProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.DeleteCellResponseProto)
  })
_sym_db.RegisterMessage(DeleteCellResponseProto)

DeleteMultiRequestProto = _reflection.GeneratedProtocolMessageType('DeleteMultiRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _DELETEMULTIREQUESTPROTO,
  '__module__' : 'com.emeraldblast.p6.proto.WorksheetProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.emeraldblast.p6.proto.DeleteMultiRequestProto)
  })
_sym_db.RegisterMessage(DeleteMultiRequestProto)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RENAMEWORKSHEETREQUESTPROTO._serialized_start=168
  _RENAMEWORKSHEETREQUESTPROTO._serialized_end=297
  _RENAMEWORKSHEETRESPONSEPROTO._serialized_start=300
  _RENAMEWORKSHEETRESPONSEPROTO._serialized_end=513
  _DELETECELLREQUESTPROTO._serialized_start=516
  _DELETECELLREQUESTPROTO._serialized_end=695
  _DELETECELLRESPONSEPROTO._serialized_start=698
  _DELETECELLRESPONSEPROTO._serialized_end=1024
  _DELETEMULTIREQUESTPROTO._serialized_start=1027
  _DELETEMULTIREQUESTPROTO._serialized_end=1261
# @@protoc_insertion_point(module_scope)
