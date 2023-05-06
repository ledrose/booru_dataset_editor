import gradio as gr
from src import *
from src.UI import *
from dataclasses import dataclass


with gr.Blocks() as demo:
    currentLoadedImage = gr.State(None)
    with gr.Row():
        searchPanel.createUI()
        selectPanel.createUI()
    searchPanel.addCallbacks(currentLoadedImage)
    selectPanel.addCallbacks(currentLoadedImage)

    
if __name__ == "__main__":
    demo.launch()