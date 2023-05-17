from scripts.MainTab import start as extStart
import gradio as gr

with gr.Blocks().queue() as demo:
    extStart()

if __name__ == '__main__':
    demo.launch()