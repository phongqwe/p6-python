# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/qxdzbc/p6/proto/AppProtos.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#com/qxdzbc/p6/proto/AppProtos.proto\x12\x13\x63om.qxdzbc.p6.proto\x1a&com/qxdzbc/p6/proto/CommonProtos.proto\x1a#com/qxdzbc/p6/proto/DocProtos.proto\"s\n\x1eSetActiveWorksheetRequestProto\x12:\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x02 \x01(\t\"\xc1\x01\n\x1fSetActiveWorksheetResponseProto\x12:\n\x0bworkbookKey\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProto\x12\x15\n\rworksheetName\x18\x02 \x01(\t\x12\x0f\n\x07isError\x18\x03 \x01(\x08\x12:\n\x0b\x65rrorReport\x18\x04 \x01(\x0b\x32%.com.qxdzbc.p6.proto.ErrorReportProto\"(\n\x18LoadWorkbookRequestProto\x12\x0c\n\x04path\x18\x01 \x01(\t\"\xb1\x01\n\x19LoadWorkbookResponseProto\x12\x39\n\x05wbKey\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProtoH\x00\x88\x01\x01\x12?\n\x0b\x65rrorReport\x18\x02 \x01(\x0b\x32%.com.qxdzbc.p6.proto.ErrorReportProtoH\x01\x88\x01\x01\x42\x08\n\x06_wbKeyB\x0e\n\x0c_errorReport\"^\n\x18SaveWorkbookRequestProto\x12\x34\n\x05wbKey\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProto\x12\x0c\n\x04path\x18\x02 \x01(\t\"\x9b\x01\n\x19SaveWorkbookResponseProto\x12:\n\x0b\x65rrorReport\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.ErrorReportProto\x12\x34\n\x05wbKey\x18\x02 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProto\x12\x0c\n\x04path\x18\x03 \x01(\t\"\xa0\x01\n\x17GetWorkbookRequestProto\x12\x39\n\x05wbKey\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProtoH\x00\x88\x01\x01\x12\x13\n\x06wbName\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07wbIndex\x18\x03 \x01(\x05H\x02\x88\x01\x01\x42\x08\n\x06_wbKeyB\t\n\x07_wbNameB\n\n\x08_wbIndex\"\xb9\x01\n!WorkbookKeyWithErrorResponseProto\x12\x39\n\x05wbKey\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProtoH\x00\x88\x01\x01\x12?\n\x0b\x65rrorReport\x18\x02 \x01(\x0b\x32%.com.qxdzbc.p6.proto.ErrorReportProtoH\x01\x88\x01\x01\x42\x08\n\x06_wbKeyB\x0e\n\x0c_errorReport\"o\n\x1d\x43reateNewWorkbookRequestProto\x12\x15\n\x08windowId\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x19\n\x0cworkbookName\x18\x02 \x01(\tH\x01\x88\x01\x01\x42\x0b\n\t_windowIdB\x0f\n\r_workbookName\"\xda\x01\n\x1e\x43reateNewWorkbookResponseProto\x12?\n\x0b\x65rrorReport\x18\x01 \x01(\x0b\x32%.com.qxdzbc.p6.proto.ErrorReportProtoH\x00\x88\x01\x01\x12\x39\n\x05wbKey\x18\x02 \x01(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProtoH\x01\x88\x01\x01\x12\x15\n\x08windowId\x18\x03 \x01(\tH\x02\x88\x01\x01\x42\x0e\n\x0c_errorReportB\x08\n\x06_wbKeyB\x0b\n\t_windowId\"T\n\x1bGetAllWorkbookResponseProto\x12\x35\n\x06wbKeys\x18\x01 \x03(\x0b\x32%.com.qxdzbc.p6.proto.WorkbookKeyProtob\x06proto3')



_SETACTIVEWORKSHEETREQUESTPROTO = DESCRIPTOR.message_types_by_name['SetActiveWorksheetRequestProto']
_SETACTIVEWORKSHEETRESPONSEPROTO = DESCRIPTOR.message_types_by_name['SetActiveWorksheetResponseProto']
_LOADWORKBOOKREQUESTPROTO = DESCRIPTOR.message_types_by_name['LoadWorkbookRequestProto']
_LOADWORKBOOKRESPONSEPROTO = DESCRIPTOR.message_types_by_name['LoadWorkbookResponseProto']
_SAVEWORKBOOKREQUESTPROTO = DESCRIPTOR.message_types_by_name['SaveWorkbookRequestProto']
_SAVEWORKBOOKRESPONSEPROTO = DESCRIPTOR.message_types_by_name['SaveWorkbookResponseProto']
_GETWORKBOOKREQUESTPROTO = DESCRIPTOR.message_types_by_name['GetWorkbookRequestProto']
_WORKBOOKKEYWITHERRORRESPONSEPROTO = DESCRIPTOR.message_types_by_name['WorkbookKeyWithErrorResponseProto']
_CREATENEWWORKBOOKREQUESTPROTO = DESCRIPTOR.message_types_by_name['CreateNewWorkbookRequestProto']
_CREATENEWWORKBOOKRESPONSEPROTO = DESCRIPTOR.message_types_by_name['CreateNewWorkbookResponseProto']
_GETALLWORKBOOKRESPONSEPROTO = DESCRIPTOR.message_types_by_name['GetAllWorkbookResponseProto']
SetActiveWorksheetRequestProto = _reflection.GeneratedProtocolMessageType('SetActiveWorksheetRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _SETACTIVEWORKSHEETREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.SetActiveWorksheetRequestProto)
  })
_sym_db.RegisterMessage(SetActiveWorksheetRequestProto)

SetActiveWorksheetResponseProto = _reflection.GeneratedProtocolMessageType('SetActiveWorksheetResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _SETACTIVEWORKSHEETRESPONSEPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.SetActiveWorksheetResponseProto)
  })
_sym_db.RegisterMessage(SetActiveWorksheetResponseProto)

LoadWorkbookRequestProto = _reflection.GeneratedProtocolMessageType('LoadWorkbookRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _LOADWORKBOOKREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.LoadWorkbookRequestProto)
  })
_sym_db.RegisterMessage(LoadWorkbookRequestProto)

LoadWorkbookResponseProto = _reflection.GeneratedProtocolMessageType('LoadWorkbookResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _LOADWORKBOOKRESPONSEPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.LoadWorkbookResponseProto)
  })
_sym_db.RegisterMessage(LoadWorkbookResponseProto)

SaveWorkbookRequestProto = _reflection.GeneratedProtocolMessageType('SaveWorkbookRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _SAVEWORKBOOKREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.SaveWorkbookRequestProto)
  })
_sym_db.RegisterMessage(SaveWorkbookRequestProto)

SaveWorkbookResponseProto = _reflection.GeneratedProtocolMessageType('SaveWorkbookResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _SAVEWORKBOOKRESPONSEPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.SaveWorkbookResponseProto)
  })
_sym_db.RegisterMessage(SaveWorkbookResponseProto)

GetWorkbookRequestProto = _reflection.GeneratedProtocolMessageType('GetWorkbookRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _GETWORKBOOKREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.GetWorkbookRequestProto)
  })
_sym_db.RegisterMessage(GetWorkbookRequestProto)

WorkbookKeyWithErrorResponseProto = _reflection.GeneratedProtocolMessageType('WorkbookKeyWithErrorResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _WORKBOOKKEYWITHERRORRESPONSEPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.WorkbookKeyWithErrorResponseProto)
  })
_sym_db.RegisterMessage(WorkbookKeyWithErrorResponseProto)

CreateNewWorkbookRequestProto = _reflection.GeneratedProtocolMessageType('CreateNewWorkbookRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _CREATENEWWORKBOOKREQUESTPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.CreateNewWorkbookRequestProto)
  })
_sym_db.RegisterMessage(CreateNewWorkbookRequestProto)

CreateNewWorkbookResponseProto = _reflection.GeneratedProtocolMessageType('CreateNewWorkbookResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _CREATENEWWORKBOOKRESPONSEPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.CreateNewWorkbookResponseProto)
  })
_sym_db.RegisterMessage(CreateNewWorkbookResponseProto)

GetAllWorkbookResponseProto = _reflection.GeneratedProtocolMessageType('GetAllWorkbookResponseProto', (_message.Message,), {
  'DESCRIPTOR' : _GETALLWORKBOOKRESPONSEPROTO,
  '__module__' : 'com.qxdzbc.p6.proto.AppProtos_pb2'
  # @@protoc_insertion_point(class_scope:com.qxdzbc.p6.proto.GetAllWorkbookResponseProto)
  })
_sym_db.RegisterMessage(GetAllWorkbookResponseProto)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SETACTIVEWORKSHEETREQUESTPROTO._serialized_start=137
  _SETACTIVEWORKSHEETREQUESTPROTO._serialized_end=252
  _SETACTIVEWORKSHEETRESPONSEPROTO._serialized_start=255
  _SETACTIVEWORKSHEETRESPONSEPROTO._serialized_end=448
  _LOADWORKBOOKREQUESTPROTO._serialized_start=450
  _LOADWORKBOOKREQUESTPROTO._serialized_end=490
  _LOADWORKBOOKRESPONSEPROTO._serialized_start=493
  _LOADWORKBOOKRESPONSEPROTO._serialized_end=670
  _SAVEWORKBOOKREQUESTPROTO._serialized_start=672
  _SAVEWORKBOOKREQUESTPROTO._serialized_end=766
  _SAVEWORKBOOKRESPONSEPROTO._serialized_start=769
  _SAVEWORKBOOKRESPONSEPROTO._serialized_end=924
  _GETWORKBOOKREQUESTPROTO._serialized_start=927
  _GETWORKBOOKREQUESTPROTO._serialized_end=1087
  _WORKBOOKKEYWITHERRORRESPONSEPROTO._serialized_start=1090
  _WORKBOOKKEYWITHERRORRESPONSEPROTO._serialized_end=1275
  _CREATENEWWORKBOOKREQUESTPROTO._serialized_start=1277
  _CREATENEWWORKBOOKREQUESTPROTO._serialized_end=1388
  _CREATENEWWORKBOOKRESPONSEPROTO._serialized_start=1391
  _CREATENEWWORKBOOKRESPONSEPROTO._serialized_end=1609
  _GETALLWORKBOOKRESPONSEPROTO._serialized_start=1611
  _GETALLWORKBOOKRESPONSEPROTO._serialized_end=1695
# @@protoc_insertion_point(module_scope)
