from com.qxdzbc.p6.document_structure.copy_paste.copier.DataFrameCopier import DataFrameCopier
from com.qxdzbc.p6.document_structure.copy_paste.copier.ProtoCopier import ProtoCopier


class Copiers:
    protoCopier = ProtoCopier()

    fullSourceDataFrameCopier = DataFrameCopier(isCopyFull = True, isCopySource = True)
    strictSourceDataFrameCopier = DataFrameCopier(isCopyFull = False, isCopySource = True)

    fullValueDataFrameCopier = DataFrameCopier(isCopyFull = True,isCopySource = False)
    strictValueDataFrameCopier = DataFrameCopier(isCopyFull = False,isCopySource = False)
