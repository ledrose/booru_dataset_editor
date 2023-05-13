from .singleton import Singleton 
from src.ImageGroup import ImageGroup
import gradio as gr

class SelectPanelUI(Singleton):
    def __init__(self):
        self.selectedImages = ImageGroup()
        self.currentImage = None

    def createUI(self):
        with gr.Column():
            self.selectedImagesGallery=gr.Gallery(
                label="Selected Images",
                show_label=True,
                elem_id='selected_gallery',
            ).style(
                columns=6, rows=4, height=300,
            )
            self.savePathTextbox = gr.Textbox(label="Save folder")
            self.tagSelectionGroup = gr.CheckboxGroup(["character","copyright","artist","meta"])
            with gr.Row():
                self.btnAddToSelected = gr.Button("Add").style(full_width=False)
                self.btnRemoveFromSelected = gr.Button("Remove").style(full_width=False)
                self.btnDownload = gr.Button("Download")


    def addCallbacks(self, currentLoadedImage):
        def addToSelect(currentLoadedImage):
            if (currentLoadedImage!=None):
                self.selectedImages.add(currentLoadedImage)
            return self.selectedImages.getGalleryTuples()

        self.btnAddToSelected.click(
            fn=addToSelect, inputs=[currentLoadedImage], outputs=[self.selectedImagesGallery]
        )

        def removeFromSelected():
            if (self.currentImage!=None):
                self.selectedImages.remove(self.currentImage)
            return self.selectedImages.getGalleryTuples()

        self.btnRemoveFromSelected.click(
            fn=removeFromSelected, inputs=[], outputs=[self.selectedImagesGallery]
        )
        def onGallerySelected(evt: gr.SelectData):
            self.currentImage = self.selectedImages.getImageByFilename(evt.value)
        
        self.selectedImagesGallery.select(
            fn=onGallerySelected, inputs=[], outputs=[]
        )

        def downloadImages(savePath):
            self.selectedImages.downloadAll(savePath)

        self.btnDownload.click(
            fn=downloadImages,inputs=[self.savePathTextbox],outputs=[]
        )
