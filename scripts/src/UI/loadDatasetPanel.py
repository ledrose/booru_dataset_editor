from . singleton import Singleton
import gradio as gr
class LoadDatasetPanelUI(Singleton):
    def __init__(self):
        pass

    def createUI(self):
        self.inputFolderTextbox = gr.Textbox('test',label='Dataset path')
        self.loadDatasetBtn = gr.Button("Load Dataset")
        self.loadedGallery = gr.Gallery()

    def addCallbacks(self):
        pass