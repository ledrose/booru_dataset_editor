from . singleton import Singleton 
from scripts.src.ImageGroup import ImageGroup
import gradio as gr

class SelectPanelUI(Singleton):
    def __init__(self):
        # self.selectedImages = ImageGroup()
        self.currentImage = None

    def createUI(self):
        self.selectedImages = gr.State(ImageGroup())
        with gr.Column():
            self.selectedImagesGallery=gr.Gallery(
                label="Selected Images",
                show_label=True,
                elem_id='selected_gallery',
            ).style(
                columns=6, rows=2,
            )
            self.savePathTextbox = gr.Textbox(label="Save folder", value='test')
            self.namePatternTexbox = gr.Textbox(label="NamePattern", value='<index>_<hash>')
            with gr.Accordion('Pattern info'):
                self.namePatternInfo = gr.Markdown("""
                    # Avaliable patterns: \n
                    \<id\> - id of image, \n
                    \<w\>, \<h\> - width and height \n
                    \<index\> - number from 0 to inf. Relies on order in which images are downloaded.\n
                    <tag_char> - character tags. If imageboard does not give then general tags\n
                    <create_date> - date of creation of post\n
                """)
            # self.tagSelectionGroup = gr.CheckboxGroup(["character","copyright","artist","meta"])
            with gr.Row():
                self.btnAddToSelected = gr.Button("Add").style(full_width=False)
                self.btnAddAllToSelected = gr.Button("Add All").style(full_width=False)
                self.btnRemoveFromSelected = gr.Button("Remove").style(full_width=False)
                self.btnClearToSelection = gr.Button("Clear Selection").style(full_width=False)
            with gr.Row():
                self.btnDownload = gr.Button("Download").style(full_width=True)


    def addCallbacks(self, currentLoadedImage, loadedImages, tagCheckboxGroup):
        def addToSelect(selectedImages, currentLoadedImage):
            if (currentLoadedImage!=None):
                selectedImages.add(currentLoadedImage)
            return [selectedImages, selectedImages.getGalleryTuples(), gr.CheckboxGroup().update(choices=selectedImages.getTagsInfo())]

        self.btnAddToSelected.click(
            fn=addToSelect, inputs=[self.selectedImages, currentLoadedImage], outputs=[self.selectedImages, self.selectedImagesGallery, tagCheckboxGroup]
        )
        def addAllToSelect(selectedImages):
            for image in loadedImages.images:
                selectedImages.add(image)
            return [selectedImages ,selectedImages.getGalleryTuples(), gr.CheckboxGroup().update(choices=selectedImages.getTagsInfo())]

        self.btnAddAllToSelected.click(
            fn=addAllToSelect, inputs=[self.selectedImages], outputs=[self.selectedImages, self.selectedImagesGallery, tagCheckboxGroup]
        )

        def removeFromSelected(selectedImages):
            if (self.currentImage!=None):
                self.currentImage = selectedImages.remove(self.currentImage)
            return [selectedImages, selectedImages.getGalleryTuples(), gr.CheckboxGroup().update(choices=selectedImages.getTagsInfo())]

        self.btnRemoveFromSelected.click(
            fn=removeFromSelected, inputs=[self.selectedImages], outputs=[self.selectedImages, self.selectedImagesGallery, tagCheckboxGroup]
        ).then(fn=lambda x: [], inputs=[tagCheckboxGroup], outputs=[tagCheckboxGroup])
        def clearSelection(selectedImages):
            selectedImages = ImageGroup()
            return [selectedImages, selectedImages.getGalleryTuples(), gr.CheckboxGroup().update(choices=selectedImages.getTagsInfo())]
        self.btnClearToSelection.click(
            fn=clearSelection, inputs=[self.selectedImages], outputs=[self.selectedImages, self.selectedImagesGallery, tagCheckboxGroup]
        ).then(fn=lambda x: [], inputs=[tagCheckboxGroup], outputs=[tagCheckboxGroup])
        def onGallerySelected(selectedImages, evt: gr.SelectData):
            self.currentImage = selectedImages.getImageByFilename(evt.value)
        
        self.selectedImagesGallery.select(
            fn=onGallerySelected, inputs=[self.selectedImages], outputs=[]
        )

        def downloadImages(selectedImages, savePath, namePattern, progress=gr.Progress(track_tqdm=True)):
            selectedImages.downloadAll(savePath, namePattern)
            return savePath

        self.btnDownload.click(
            fn=downloadImages,inputs=[self.selectedImages, self.savePathTextbox, self.namePatternTexbox],outputs=[self.savePathTextbox]
        )
