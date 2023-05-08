from .singleton import Singleton
from src import Imageboard
from src.ConfigManager import ConfigManager
import gradio as gr

class TopPanelUI(Singleton):
    def __init__(self):
        self.imageboardList = ConfigManager.getImageboardsFromJson('imagebords.json')

    def createUI(self):
        self.selectImageboard = gr.Dropdown([x.name for x in self.imageboardList],multiselect=False, interactive=True,label="Выбор имиджборда", value="Testbooru")
        self.saveImageboardsButton = gr.Button("Save Imageboards")

    def addCallbacks(self, imageboard):
        def changeImageboard(evt: gr.SelectData):
            return self.imageboardList[evt.index]
            
        self.selectImageboard.select(
            fn=changeImageboard, inputs=[], outputs=[imageboard]
        )
        def saveImageboards():
            ConfigManager.saveImageboardsToJson("imagebords.json", self.imageboardList)

        self.saveImageboardsButton.click(
            fn=saveImageboards, inputs=[], outputs=[]
        )