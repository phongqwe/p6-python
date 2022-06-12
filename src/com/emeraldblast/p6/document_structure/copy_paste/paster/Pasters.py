from com.emeraldblast.p6.document_structure.copy_paste.paster.AllPaster import AllPaster
from com.emeraldblast.p6.document_structure.copy_paste.paster.DataFramePaster import DataFramePaster
from com.emeraldblast.p6.document_structure.copy_paste.paster.ProtoPaster import ProtoPaster
from com.emeraldblast.p6.document_structure.copy_paste.paster.TextPaster import TextPaster


class Pasters:
    protoPaster = ProtoPaster()
    dataFramePaster = DataFramePaster()
    textPaster = TextPaster()
    allPaster = AllPaster(
        protoPaster = protoPaster,
        textPaster = textPaster,
        dfPaster = dataFramePaster
    )