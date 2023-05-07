from .singleton import Singleton
from src import Imageboard
import gradio as gr

class TopPanelUI(Singleton):
    def __init__(self):
        self.imageboardList = [
            Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu"),
            Imageboard("Danbooru", "https://danbooru.donmai.us", login="ledrose", apiKey="gBHJNPPPMAiy4HBzsS7RyyZk")
        ]

    def createUI(self):
        self.selectImageboard = gr.Dropdown([x.name for x in self.imageboardList],multiselect=False, interactive=True,label="Выбор имиджборда", value="Testbooru")

    def addCallbacks(self, imageboard):
        def changeImageboard(evt: gr.SelectData):
            return self.imageboardList[evt.index]
            
        self.selectImageboard.select(
            fn=changeImageboard, inputs=[], outputs=[imageboard]
        )