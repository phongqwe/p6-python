from com.emeraldblast.p6.document_structure.copy_paste.paster.UnifiedPaster import UnifiedPaster
from com.emeraldblast.p6.document_structure.copy_paste.paster.DataFramePaster import DataFramePaster
from com.emeraldblast.p6.document_structure.copy_paste.paster.ProtoPaster import ProtoPaster
from com.emeraldblast.p6.document_structure.copy_paste.paster.TextPaster import TextPaster


class Pasters:
    protoPaster = ProtoPaster()
    dataFramePaster = DataFramePaster()
    textPaster = TextPaster()
    unifiedPaster = UnifiedPaster(
        protoPaster = protoPaster,
        textPaster = textPaster,
        dfPaster = dataFramePaster
    )