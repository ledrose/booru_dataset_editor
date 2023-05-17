from . singleton import Singleton
import gradio as gr

class TagEditPanelUI(Singleton):
    def __init__(self):
        pass

    def createUI(self):
        self.tagCheckboxGroup = gr.CheckboxGroup(['1','2','3'], label='Tags')
        self.modeRadio = gr.Radio(choices=['AND', 'OR'], value='AND', label="Mode of tag selection")

    def addCallbacks(self):
        pass