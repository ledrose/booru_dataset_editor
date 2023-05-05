import gradio as gr
from src import *
from src.UI import *
from dataclasses import dataclass

def addToSelect():
    if (searchPanel.currentImage!=None):
        selectPanel.selectedImages.add(searchPanel.currentImage)
    return [searchPanel.loadedImageboard.getImageWithFilename(x).getImageTuple() for x in selectPanel.selectedImages]

def removeFromSelected():
    if (selectPanel.currentImage!=None):
        selectPanel.selectedImages.remove(selectPanel.currentImage)
    return [searchPanel.loadedImageboard.getImageWithFilename(x).getImageTuple() for x in selectPanel.selectedImages]

def downloadImages(savePath):
    for x in selectPanel.selectedImages:
        searchPanel.loadedImageboard.getImageWithFilename(x).saveImageWithTags(savePath)

with gr.Blocks() as demo:
    with gr.Row():
        searchPanel.createUI()
        selectPanel.createUI()
    searchPanel.addCallbacks()
    selectPanel.addCallbacks(addToSelect, removeFromSelected, downloadImages)
    
if __name__ == "__main__":
    demo.launch()