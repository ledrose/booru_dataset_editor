from .singleton import Singleton 
import gradio as gr

class SelectPanelUI(Singleton):
    def __init__(self):
        self.selectedImages = set()
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
            with gr.Row():
                self.btnAddToSelected = gr.Button("Add").style(full_width=False)
                self.btnRemoveFromSelected = gr.Button("Remove").style(full_width=False)
                self.btnDownload = gr.Button("Download")


    def addCallbacks(self, addToSelect, removeFromSelected, downlaodImages):
        self.btnAddToSelected.click(
            fn=addToSelect, inputs=[], outputs=[self.selectedImagesGallery]
        )
        def onGallerySelected(evt: gr.SelectData):
            self.currentImage = evt.value

        self.selectedImagesGallery.select(
            fn=onGallerySelected, inputs=[], outputs=[]
        )

        self.btnRemoveFromSelected.click(
            fn=removeFromSelected, inputs=[], outputs=[self.selectedImagesGallery]
        )
        self.btnDownload.click(
            fn=downlaodImages,inputs=[self.savePathTextbox],outputs=[]
        )
