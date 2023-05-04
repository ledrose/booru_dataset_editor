import gradio as gr
from src.Imageboard import Imageboard

iboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")

def test(str, pageNum, imgCount):
    iboard.requestImageSearch(str, pageNum, imgCount)
    return iboard.getImageLinks()

def onSelect(selectedImage, evt: gr.SelectData):
        return [
            evt.index,
            f"You selected {evt.value} at {evt.index} from {evt.target}",
        ]

def downloadSelected(selectedImage):
    try:
        iboard.getImageWithId(selectedImage).saveImageWithTags('./test')
        return [selectedImage,"Ok"]
    except:
        return [selectedImage,"Error"]

def previousPage(curPage):
    return (curPage - 1) if curPage>1 else curPage

def nextPage(curPage):
    return (curPage + 1) if curPage<100 else curPage

with gr.Blocks() as demo:
    selectedImage = gr.State(None)
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
                elem_id='gallery').style(
                    columns=[4], rows=[4], object_fit='contain', height=300
                )
            with gr.Row():
                buttonPrev = gr.Button("Previous Page").style(full_width=False) #TODO
                pageNumSlider = gr.Slider(1,100, step=1, label="Current page")
                buttonNext = gr.Button("Next Page").style(full_width=False) #TODO
            
    btnRequest.click(test, inputs=[request, pageNumSlider, imgCountSlider], outputs=[gallery])
    btnDownload.click(downloadSelected, inputs=[selectedImage], outputs=[selectedImage, statusTexbox])
    buttonPrev.click(previousPage, inputs=[pageNumSlider], outputs=[pageNumSlider])
    buttonNext.click(nextPage, inputs=[pageNumSlider], outputs=[pageNumSlider])
    gallery.select(
        fn=onSelect,
        inputs=[selectedImage],
        outputs=[selectedImage,testOnSelect]
    )
    

if __name__ == "__main__":
    demo.launch()