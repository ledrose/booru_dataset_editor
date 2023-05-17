from . ui_classes import *

__all__ = [
    "searchPanel",
    "selectPanel",
    "topPanel",
    "tagEditPanel"
    # "imageboardTab"
]

searchPanel = SearchPanelUI.getInstance()
selectPanel = SelectPanelUI.getInstance()
topPanel = TopPanelUI().getInstance()
tagEditPanel = TagEditPanelUI().getInstance()
# imageboardTab = ImageboardTabUI.getInstance()