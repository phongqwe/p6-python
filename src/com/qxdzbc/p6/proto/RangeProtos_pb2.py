# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/qxdzbc/p6/proto/RangeProtos.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%com/qxdzbc/p6/proto/RangeProtos.proto\x12\x13\x63om.qxdzbc.p6.proto\x1a&com/qxdzbc/p6/proto/CommonProtos.proto\x1a#com/qxdzbc/p6/proto/DocProtos.proto\"t\n\x1aRangeOperationRequestProto\x12\x32\n\x07rangeId\x18\x01 \x01(\x0b\x32!.com.qxdzbc.p6.proto.RangeIdProto\x12\x15\n\x08windowId\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_windowId\"\xb9\x01\n\x1dRangeToClipboardResponseProto\x12@\n\x0e\x65rrorIndicator\x18\x01 \x01(\x0b\x32(.com.qxdzbc.p6.proto.ErrorIndicatorProto\x12\x32\n\x07rangeId\x18\x02 \x01(\x0b\x32!.com.qxdzbc.p6.proto.RangeIdProto\x12\x15\n\x08windowId\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_windowId\"m\n\x0eRangeCopyProto\x12-\n\x02id\x18\x01 \x01(\x0b\x32!.com.qxdzbc.p6.proto.RangeIdProto\x12,\n\x04\x63\x65ll\x18\x02 \x03(\x0b\x32\x1e.com.qxdzbc.p6.proto.CellProto\"\xa5\x01\n\x16PasteRangeRequestProto\x12\x39\n\nanchorCell\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.CellAddressProto\x12,\n\x04wsWb\x18\x02 \x01(\x0b\x32\x1e.com.qxdzbc.p6.proto.WsWbProto\x12\x15\n\x08windowId\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_windowIdb\x06proto3')



_RANGEOPERATIONREQUESTPROTO = DESCRIPTOR.message_types_by_name['RangeOperationRequestProto']
_RANGETOCLIPBOARDRESPONSEPROTO = DESCRIPTOR.message_types_by_name['RangeToClipboardResponseProto']
_RANGECOPYPROTO = DESCRIPTOR.message_types_by_name['RangeCopyProto']
_PASTERANGEREQUESTPROTO = DESCRIPTOR.message_types_by_name['PasteRangeRequestProto']
RangeOperationRequestProto = _reflection.GeneratedProtocolMessageType('RangeOperationRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _RANGEOPERATIONREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.RangeProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.RangeOperationRequestProto)
  })
_sym_db.RegisterMessage(RangeOperationRequestProto)

RangeToClipboardResponseProto = _reflection.GeneratedProtocolMessageType('RangeToClipboardResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _RANGETOCLIPBOARDRESPONSEPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.RangeProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.RangeToClipboardResponseProto)
  })
_sym_db.RegisterMessage(RangeToClipboardResponseProto)

RangeCopyProto = _reflection.GeneratedProtocolMessageType('RangeCopyProto', (_message.Message,), {
  'DESCRIPTOR' : _RANGECOPYPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.RangeProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.RangeCopyProto)
  })
_sym_db.RegisterMessage(RangeCopyProto)

PasteRangeRequestProto = _reflection.GeneratedProtocolMessageType('PasteRangeRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _PASTERANGEREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.RangeProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.PasteRangeRequestProto)
  })
_sym_db.RegisterMessage(PasteRangeRequestProto)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RANGEOPERATIONREQUESTPROTO._serialized_start=139
  _RANGEOPERATIONREQUESTPROTO._serialized_end=255
  _RANGETOCLIPBOARDRESPONSEPROTO._serialized_start=258
  _RANGETOCLIPBOARDRESPONSEPROTO._serialized_end=443
  _RANGECOPYPROTO._serialized_start=445
  _RANGECOPYPROTO._serialized_end=554
  _PASTERANGEREQUESTPROTO._serialized_start=557
  _PASTERANGEREQUESTPROTO._serialized_end=722
# @@protoc_insertion_point(module_scope)
