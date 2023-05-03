import gradio as gr
from src.Imageboard import Imageboard

iboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")

def test(str):
    iboard.requestImageSearch(str)
    return iboard.getImageLinks()

with gr.Blocks() as demo:
    with gr.Row(variant="compact"):
        with gr.Column():
            request = gr.Textbox(
                label="Enter your search request",
                show_label=False,
                placeholder="Enter your search request",
                max_lines=1)
            btn = gr.Button("Request images").style(full_width=False)
        gallery = gr.Gallery(
            label="Search results",
            show_label=False,
            elem_id='gallery').style(
                columns=[4], rows=[4], object_fit='contain', height=300
            )
    btn.click(test, inputs=[request], outputs=[gallery])


if __name__ == "__main__":
    demo.launch()