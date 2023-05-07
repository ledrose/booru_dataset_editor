from .ui_classes import *

__all__ = [
    "searchPanel",
    "selectPanel",
    "topPanel"
    # "imageboardTab"
]

searchPanel = SearchPanelUI.getInstance()
selectPanel = SelectPanelUI.getInstance()
topPanel = TopPanelUI().getInstance()
# imageboardTab = ImageboardTabUI.getInstance()