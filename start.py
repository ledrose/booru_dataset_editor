import gradio as gr
from src.Imageboard import Imageboard
from dataclasses import dataclass

selectedStyle = 'background-color: grey;'
iboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")


def getPosts(selectedImages: list[int], request: str, pageNum: int, imgCount: int):
    selectedImages = []
    iboard.requestImageSearch(request, pageNum, imgCount)
    return [selectedImages, iboard.getImageLinks()]

def onSelect(selectedImages: list[int], evt: gr.SelectData):
    respStr = ""
    if (selectedImages.count(evt.index)>=1):
        selectedImages.remove(evt.index)
        respStr = f"You removed {evt.value} at {evt.index} from {evt.target}"
    else:
        selectedImages.append(evt.index)
        respStr = f"You selected {evt.value} at {evt.index} from {evt.target}"
    return [
        selectedImages,
        respStr,
    ]

def downloadSelected(selectedImages: list[int]):
    try:
        for index in selectedImages:
            iboard.getImageWithId(index).saveImageWithTags('./test')
        return [selectedImages,"Ok"]
    except:
        return [selectedImages,"Error"]

def previousPage(curPage):
    return (curPage - 1) if curPage>1 else curPage

def nextPage(curPage):
    return (curPage + 1) if curPage<100 else curPage

with gr.Blocks(css=".test {background-color: red}") as demo:
    selectedImages = gr.State([])
    with gr.Row(variant="compact"):
        with gr.Column():
            request = gr.Textbox(
                label="Enter your search request",
                show_label=False,
                placeholder="Enter your search request",
                max_lines=1)
            with gr.Row():
                imgCountSlider = gr.Slider(1, 50, value=20, step=1, label="Number of shown images")
                btnRequest = gr.Button("Request images").style(full_width=False)
            testOnSelect = gr.Textbox()
            statusTexbox = gr.Textbox()
            btnDownload = gr.Button("Download selected image")
        with gr.Column():
            gallery = gr.Gallery(
                label="Search results",
                show_label=False,
                elem_id='gallery',
                elem_classes="test",
                ).style(
                    columns=[4], rows=[4], object_fit='contain', height=300
                )
            with gr.Row():
                buttonPrev = gr.Button("Previous Page").style(full_width=False) #TODO
                pageNumSlider = gr.Slider(1,100, step=1, label="Current page")
                buttonNext = gr.Button("Next Page").style(full_width=False) #TODO
            
    btnRequest.click(getPosts, inputs=[selectedImages, request, pageNumSlider, imgCountSlider], outputs=[selectedImages, gallery])
    btnDownload.click(downloadSelected, inputs=[selectedImages], outputs=[selectedImages, statusTexbox])
    buttonPrev.click(previousPage, inputs=[pageNumSlider], outputs=[pageNumSlider])
    buttonNext.click(nextPage, inputs=[pageNumSlider], outputs=[pageNumSlider])
    gallery.select(
        fn=onSelect,
        inputs=[selectedImages],
        outputs=[selectedImages,testOnSelect]
    )
    

if __name__ == "__main__":
    demo.launch()