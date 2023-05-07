from .singleton import Singleton
from src import Imageboard, ImageGroup
import gradio as gr

testImageboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")


class SearchPanelUI(Singleton):
    def __init__(self):
        # self.loadedImageboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")
        self.loadedImages = ImageGroup()

    def createUI(self):
        with gr.Column():
            self.loadedImagesGallery = gr.Gallery(
                label="Search results",
                show_label=True,
                elem_id='gallery',
            ).style(
                columns=[6], rows=[4], object_fit='contain', height=300
            )
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

    def addCallbacks(self, currentLoadedImage, loadedImageboard):
        print(loadedImageboard)
        def getPosts(loadedImageboard, searchInput, imgCount, pageNum):
            self.loadedImages.images = loadedImageboard.requestImageSearch(searchInput=searchInput,imgCount=imgCount, pageNum=pageNum)
            return self.loadedImages.getGalleryTuples()
        self.btnRequestPosts.click(
            fn=getPosts, inputs=[loadedImageboard, self.searchRequestTextbox, self.imgCountSlider, self.curPageSlider], outputs=[self.loadedImagesGallery]
        )
        def onGallerySelected(evt: gr.SelectData):
            return self.loadedImages.getImageByFilename(evt.value)

        self.loadedImagesGallery.select(fn=onGallerySelected,inputs=None, outputs=[currentLoadedImage])
        