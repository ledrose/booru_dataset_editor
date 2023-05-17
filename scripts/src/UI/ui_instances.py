from . ui_classes import *

__all__ = [
    "searchPanel",
    "selectPanel",
    "topPanel",
    "loadDatasetPanel"
    # "imageboardTab"
]

searchPanel = SearchPanelUI.getInstance()
selectPanel = SelectPanelUI.getInstance()
topPanel = TopPanelUI().getInstance()
loadDatasetPanel = LoadDatasetPanelUI().getInstance()
# imageboardTab = ImageboardTabUI.getInstance()