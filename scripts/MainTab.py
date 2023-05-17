import gradio as gr
from scripts.src import *
from scripts.src.UI import *
from dataclasses import dataclass


def start():
    currentLoadedImage = gr.State(None)
    with gr.Column():
        imageboard = gr.State(topPanel.imageboardList[0])
        with gr.Row():
            with gr.Tab("Imageboard"):
                with gr.Column():
                    topPanel.createUI()
                    searchPanel.createUI()
            with gr.Tab("Tags"):
                tagEditPanel.createUI()
            selectPanel.createUI()
    topPanel.addCallbacks(imageboard)
    searchPanel.addCallbacks(currentLoadedImage, imageboard, selectPanel.savePathTextbox)
    selectPanel.addCallbacks(currentLoadedImage, searchPanel.loadedImages, tagEditPanel.tagCheckboxGroup)
    tagEditPanel.addCallbacks()

