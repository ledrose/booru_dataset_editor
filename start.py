import gradio as gr
from src.Imageboard import Imageboard

iboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")

def getPosts(selectedImages: list[int], request: str, pageNum: int, imgCount: int):
    iboard.requestImageSearch(request, pageNum, imgCount)
    return [selectedImages, iboard.getImageLinks()]

def onSelect(evt: gr.SelectData, gallerySelected: list[tuple[str, str]], modeRadio:str, selectedImages: list[str]):
    respStr = "Nothing happend"
    print(evt.value)
    if (modeRadio=='Selection'):
        if (selectedImages.count(iboard.getImageWithName(evt.value).imgLink)>=1):
            selectedImages.remove(iboard.getImageWithName(evt.value).imgLink)
            respStr = f"You removed {evt.value} at {evt.index} from {evt.target}"
        else:
            selectedImages.append(iboard.getImageWithName(evt.value).imgLink)
            respStr = f"You selected {evt.value} at {evt.index} from {evt.target}"
    return [
        selectedImages,
        selectedImages,
        respStr,
    ]

def downloadSelected(selectedImages: list[str]):
    try:
        for name in selectedImages:
            iboard.getImageWithName(name).saveImageWithTags('./test')
        return [selectedImages,"Ok"]
    except:
        return [selectedImages,"Error"]

def previousPage(curPage: int):
    return (curPage - 1) if curPage>1 else curPage

def nextPage(curPage: int):
    return (curPage + 1) if curPage<100 else curPage

with gr.Blocks() as demo:
    selectedImages = gr.State([])
    with gr.Row(variant="compact"):
        with gr.Column():
            request = gr.Textbox(
                label="Enter your search request",
                show_label=False,
                placeholder="Enter your search request",
                max_lines=1)
            with gr.Row():
                imgCountSlider = gr.Slider(1, 50, value=10, step=1, label="Number of shown images")
                btnRequest = gr.Button("Request images").style(full_width=False)
            modeRadio = gr.Radio(choices=['Preview','Selection'],label="Mode of action", value='Preview', interactive=True)
            testOnSelect = gr.Textbox()
            statusTexbox = gr.Textbox()
            btnDownload = gr.Button("Download selected image")
        with gr.Column():
            gallery = gr.Gallery(
                label="Search results",
                show_label=False,
                elem_id='gallery',
                ).style(
                    columns=6, rows=4, object_fit='contain', height=300, preview=False,
                )
            with gr.Row():
                buttonPrev = gr.Button("Previous Page").style(full_width=False) #TODO
                pageNumSlider = gr.Slider(1,100, step=1, label="Current page")
                buttonNext = gr.Button("Next Page").style(full_width=False) #TODO
            gallerySelected = gr.Gallery(
                label="Selected Images",
                elem_id='galerySelected',
                value=[]
                ).style(
                columns=6, rows=1, object_fit='contain', height=300,
                )
    btnRequest.click(getPosts, inputs=[selectedImages, request, pageNumSlider, imgCountSlider], outputs=[selectedImages, gallery])
    btnDownload.click(downloadSelected, inputs=[selectedImages], outputs=[selectedImages, statusTexbox])
    buttonPrev.click(previousPage, inputs=[pageNumSlider], outputs=[pageNumSlider])
    buttonNext.click(nextPage, inputs=[pageNumSlider], outputs=[pageNumSlider])
    gallery.select(
        fn=onSelect,
        inputs=[gallerySelected,modeRadio, selectedImages],
        outputs=[gallerySelected, selectedImages,testOnSelect]
    )
    

if __name__ == "__main__":
    demo.launch()