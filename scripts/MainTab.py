import gradio as gr
from scripts.src import *
from scripts.src.UI import *
from dataclasses import dataclass


def start():
    with gr.Tab('Download'):
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
    with gr.Tab('Dataset Work'):
        loadDatasetPanel.createUI()
        loadDatasetPanel.addCallbacks()

