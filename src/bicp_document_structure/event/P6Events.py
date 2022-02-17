from bicp_document_structure.event.P6Event import P6Event


class P6Events:
    class Cell:
        UpdateValue = P6Event("Update cell value", "e0")
        UpdateScript = P6Event("Update cell script", "e1")
        UpdateFormula = P6Event("Update cell formula", "e2")
        ClearScriptResult = P6Event("Clear cell script result", "e3")