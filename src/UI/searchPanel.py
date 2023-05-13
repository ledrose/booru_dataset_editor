from .singleton import Singleton
from src import Imageboard, ImageGroup
import gradio as gr

def getNewFileName(inp, filename, oldname):
    out = []
    for [img, name] in inp:
        if (name==filename):
            return img['name']
    return oldname


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
                label="Enter your search request",
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
                        self.btnQuickDownload = gr.Button("Quick Download").style(full_width=False)

    def addCallbacks(self, currentLoadedImage, loadedImageboard, savePathTextbox):
        def getPosts(loadedImageboard, searchInput, imgCount, pageNum):
            self.loadedImages.images = loadedImageboard.requestImageSearch(searchInput=searchInput,imgCount=imgCount, pageNum=pageNum)
            return self.loadedImages.getGalleryTuples()
        self.btnRequestPosts.click(
            fn=getPosts, inputs=[loadedImageboard, self.searchRequestTextbox, self.imgCountSlider, self.curPageSlider], outputs=[self.loadedImagesGallery]
        )
        def onGallerySelected(evt: gr.SelectData, loadedImagesGallery: list):
            # print(getNewFileName(loadedImagesGallery, evt.value))
            image = self.loadedImages.getImageByFilename(evt.value)
            image.localFile = getNewFileName(loadedImagesGallery, evt.value, None)
            return image

        self.loadedImagesGallery.select(fn=onGallerySelected,inputs=[self.loadedImagesGallery], outputs=[currentLoadedImage])

        def quickDownload(loadedImageboard, searchInput, imgCount, pageNum, savepath):
            qdImages = ImageGroup(loadedImageboard.requestImageSearch(searchInput=searchInput,imgCount=imgCount, pageNum=pageNum))
            qdImages.downloadAll(savepath)

        self.btnQuickDownload.click(
            fn=quickDownload, inputs=[loadedImageboard, self.searchRequestTextbox, self.imgCountSlider, self.curPageSlider, savePathTextbox], outputs = None
        )
        