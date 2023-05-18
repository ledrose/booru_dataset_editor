from . singleton import Singleton
import gradio as gr

class TagEditPanelUI(Singleton):
    def __init__(self):
        pass

    def createUI(self):
        with gr.Accordion('Replace tags', open=False):
            self.replaceSourceTextBox = gr.Textbox(label='What to replace', placeholder='tags separated by comma', info='If there is no corresponding tag in second box, that tag will be removed')
            self.replaceDestTextBox = gr.Textbox(label='Replace with what', placeholder='tags separated by comma', info='If there is no corresponding tag in first box, that tag will be added')
            self.replaceConfirmBtn = gr.Button('Apply replacement')
        with gr.Row():
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
        def replaceTags(source, dest, selectedImages):
            selectedImages.replaceTags(source, dest)
            return [selectedImages, gr.CheckboxGroup().update(choices=selectedImages.getTagsInfo())]
        self.replaceConfirmBtn.click(
            fn=replaceTags, inputs=[self.replaceSourceTextBox, self.replaceDestTextBox, selectedImages], outputs=[selectedImages, self.tagCheckboxGroup]
        )