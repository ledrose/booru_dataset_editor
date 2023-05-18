from . singleton import Singleton
import gradio as gr

class TagEditPanelUI(Singleton):
    def __init__(self):
        pass

    def createUI(self):
        self.modeRadio = gr.Radio(choices=['NONE','AND', 'OR'], value='NONE', label="Mode of tag selection")
        self.btnClearSelection = gr.Button('Clear Selection')
        self.tagCheckboxGroup = gr.CheckboxGroup(label='Tags')

    def addCallbacks(self, selectedImages, selectedImagesGallery):
        def onCheckboxChange(selectedImages, tagCheckboxGroup, modeRadio):
            selectedImages.filter = [x.rpartition(' ')[0] for x in tagCheckboxGroup] 
            # print(selectedImages.filter)
            selectedImages.filterType = modeRadio
            return [selectedImages, selectedImages.getGalleryTuples()]
        self.tagCheckboxGroup.change(
            fn=onCheckboxChange, inputs=[selectedImages, self.tagCheckboxGroup,self.modeRadio], outputs=[selectedImages, selectedImagesGallery]
        )
        self.modeRadio.change(
            fn=onCheckboxChange, inputs=[selectedImages, self.tagCheckboxGroup,self.modeRadio], outputs=[selectedImages, selectedImagesGallery]
        )
        def clearSelection(selectedImages):
            selectedImages.filter = None
            selectedImages.filterType = None
            return [selectedImages, selectedImages.getGalleryTuples(), [], "NONE"]
        self.btnClearSelection.click(
            fn=clearSelection, inputs=[selectedImages], outputs=[selectedImages, selectedImagesGallery, self.tagCheckboxGroup, self.modeRadio]
        )