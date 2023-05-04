import gradio as gr
from src.Imageboard import Imageboard

iboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")

def test(str):
    iboard.requestImageSearch(str)
    return iboard.getImageLinks()


def downloadSelected(selectedImage):
    try:
        iboard.getImageWithId(selectedImage).saveImageWithTags('./test')
        return [selectedImage,"Ok"]
    except:
        return [selectedImage,"Error"]

with gr.Blocks() as demo:
    selectedImage = gr.State(None)
    def onSelect(selectedImage, evt: gr.SelectData):
        return [
            evt.index,
            f"You selected {evt.value} at {evt.index} from {evt.target}",
        ]
    with gr.Row(variant="compact"):
        with gr.Column():
            request = gr.Textbox(
                label="Enter your search request",
                show_label=False,
                placeholder="Enter your search request",
                max_lines=1)
            btnRequest = gr.Button("Request images").style(full_width=False)
            testOnSelect = gr.Textbox()
            statusTexbox = gr.Textbox()
            btnDownload = gr.Button("Download selected image")
        gallery = gr.Gallery(
            label="Search results",
            show_label=False,
            elem_id='gallery').style(
                columns=[4], rows=[4], object_fit='contain', height=300
            )
        gallery.select(
            fn=onSelect,
            inputs=[selectedImage],
            outputs=[selectedImage,testOnSelect])
    btnRequest.click(test, inputs=[request], outputs=[gallery])
    btnDownload.click(downloadSelected, inputs=[selectedImage], outputs=[selectedImage, statusTexbox])

if __name__ == "__main__":
    demo.launch()