from .singleton import Singleton
from src import Imageboard
import gradio as gr


class SearchPanelUI(Singleton):
    def __init__(self):
        self.loadedImageboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")
        self.currentImage = None
        self.selectedImages = set()

    def createUI(self):
        with gr.Row():
            with gr.Column():
                self.searchRequestTextbox = gr.Textbox(
                    label="Enter nyour search request",
                    show_label=False,
                    placeholder="Enter your search request",
                    max_lines=1
                )
                with gr.Row():
                    with gr.Column():
                        self.imgCountSlider = gr.Slider(1, 50, value=20, step=1, label="Number of shown images")
                        self.curPageSlider = gr.Slider(1,100, step=1, label="Current page")
                        with gr.Row():
                            self.btnRequestPosts = gr.Button("Search").style(full_width=False)
                            self.btnTemp = gr.Button("Add to list").style(full_width=False)
            self.loadedImagesGallery = gr.Gallery(
                label="Search results",
                show_label=True,
                elem_id='gallery',
            ).style(
                columns=[6], rows=[4], object_fit='contain', height=300
            )

    def addCallbacks(self):
        def getPosts(searchInput, imgCount, pageNum):
            self.loadedImageboard.requestImageSearch(searchInput=searchInput,imgCount=imgCount, pageNum=pageNum)
            return self.loadedImageboard.getImageLinks()
        self.btnRequestPosts.click(
            fn=getPosts, inputs=[self.searchRequestTextbox, self.imgCountSlider, self.curPageSlider], outputs=[self.loadedImagesGallery]
        )
        def onGallerySelected(evt: gr.SelectData):
            self.currentImage = evt.value
            infoStr = f"You selected {evt.value} at {evt.index} from {evt.target}"
            # print(infoStr)
            print(self.currentImage)
            print(self.selectedImages)
            return None
        self.loadedImagesGallery.select(fn=onGallerySelected,inputs=None, outputs=None)
        def onBtnTmpClick():
            if (self.currentImage==None):
                return None
            if self.currentImage in self.selectedImages:
                self.selectedImages.remove(self.currentImage)
                return None
            self.selectedImages.add(self.currentImage)
            return None

        self.btnTemp.click(fn=onBtnTmpClick, inputs=[], outputs=[])