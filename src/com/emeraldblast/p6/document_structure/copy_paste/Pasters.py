from com.emeraldblast.p6.document_structure.copy_paste.AllPaster import AllPaster
from com.emeraldblast.p6.document_structure.copy_paste.DataFramePaster import DataFramePaster
from com.emeraldblast.p6.document_structure.copy_paste.ProtoPaster import ProtoPaster
from com.emeraldblast.p6.document_structure.copy_paste.TextPaster import TextPaster


class Pasters:
    protoPaster = ProtoPaster()
    dataFramePaster = DataFramePaster()
    textPaster = TextPaster()
    allPaster = AllPaster(
        protoPaster = protoPaster,
        textPaster = textPaster,
        dfPaster = dataFramePaster
    )