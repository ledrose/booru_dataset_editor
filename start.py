import gradio as gr
from src import *
from src.UI import *
from dataclasses import dataclass


with gr.Blocks() as demo:
    currentLoadedImage = gr.State(None)
    imageboard = gr.State(Imageboard("Danbooru", "https://danbooru.donmai.us", login="ledrose", apiKey="gBHJNPPPMAiy4HBzsS7RyyZk"))
    with gr.Column():
        topPanel.createUI()
        with gr.Row():
            searchPanel.createUI()
            selectPanel.createUI()
    topPanel.addCallbacks(imageboard)
    searchPanel.addCallbacks(currentLoadedImage, imageboard)
    selectPanel.addCallbacks(currentLoadedImage)
    
if __name__ == "__main__":
    demo.launch()