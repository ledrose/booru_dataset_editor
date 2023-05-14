import gradio as gr
from src import *
from src.UI import *
from dataclasses import dataclass


with gr.Blocks() as demo:
    currentLoadedImage = gr.State(None)
    with gr.Column():
        topPanel.createUI()
        imageboard = gr.State(topPanel.imageboardList[0])
        with gr.Row():
            searchPanel.createUI()
            selectPanel.createUI()
    topPanel.addCallbacks(imageboard)
    searchPanel.addCallbacks(currentLoadedImage, imageboard, selectPanel.savePathTextbox)
    selectPanel.addCallbacks(currentLoadedImage, searchPanel.loadedImages)
    
if __name__ == "__main__":
    demo.launch()