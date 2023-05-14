from .singleton import Singleton
from src.Imageboard import factoryDict
from src import Imageboard
from src.ConfigManager import ConfigManager
import gradio as gr

class TopPanelUI(Singleton):
    def __init__(self):
        self.imageboardList = ConfigManager.getImageboardsFromJson('imagebords.json')

    def createUI(self):
        with gr.Row():
            self.selectImageboard = gr.Dropdown([x.name for x in self.imageboardList],multiselect=False, interactive=True,label="Выбор имиджборда", value=self.imageboardList[0].name)
            with gr.Accordion("Edit or add new imageboard", open=False):
                with gr.Column():
                    with gr.Row(variant="panel"):
                        self.imageboardName = gr.Textbox(label="visible name", value=self.imageboardList[0].name)
                        self.imageboardMainLink  = gr.Textbox(label="main link", value=self.imageboardList[0].mainLink)
                    with gr.Row(variant="panel"):
                        self.imageboardTypeList = gr.Dropdown(label="Imageboard type", interactive=True, choices=factoryDict.keys(), value=self.imageboardList[0].type)
                        self.imageboardUsername = gr.Textbox(label="username", value=self.imageboardList[0].user['login'] if self.imageboardList[0].user!=None else "")
                        self.imageobardApiKey = gr.Textbox(label="api key", value=self.imageboardList[0].user['apiKey'] if self.imageboardList[0].user!=None else "")
                    with gr.Row(variant="panel"):
                        self.saveImageboardsButton = gr.Button("Update Imageboard")
                        self.deleteImageboardButton = gr.Button("Delete Imageboard")
                        self.addNewImageboardButton = gr.Button("Add new imageboard")


    def addCallbacks(self, imageboard):
        def changeImageboard(evt: gr.SelectData):
            imgboard = self.imageboardList[evt.index]
            return [imgboard, imgboard.type, imgboard.name, imgboard.mainLink, imgboard.user['login'] if imgboard.user!=None else "", imgboard.user['apiKey'] if imgboard.user!=None else ""]

        self.selectImageboard.select(
            fn=changeImageboard, inputs=[], outputs=[imageboard, self.imageboardTypeList, self.imageboardName,self.imageboardMainLink, self.imageboardUsername, self.imageobardApiKey]
        )
        def saveImageboards():
            ConfigManager.saveImageboardsToJson("imagebords.json", self.imageboardList)

        self.saveImageboardsButton.click(
            fn=saveImageboards, inputs=[], outputs=[]
        )
        def addNewImageboard(type, name, mainLink, username, apiKey):
            self.imageboardList.append(factoryDict[type](name, mainLink,login=username, apiKey=apiKey))
            ConfigManager.saveImageboardsToJson('imagebords.json', self.imageboardList)
            return gr.Dropdown.update(choices=[x.name for x in self.imageboardList])
        
        self.addNewImageboardButton.click(
            fn=addNewImageboard, inputs=[self.imageboardTypeList, self.imageboardName,self.imageboardMainLink, self.imageboardUsername, self.imageobardApiKey], outputs=[self.selectImageboard]
        )
        def deleteImageboard(imgboard, type, selectImgboard, name, mainLink, username, apiKey):
            if (len(self.imageboardList)<=1):
                return [imgboard, type, selectImgboard, name, mainLink, username, apiKey]
            self.imageboardList.remove(imgboard)
            ConfigManager.saveImageboardsToJson('imagebords.json', self.imageboardList)
            cur = self.imageboardList[0]
            return [cur, gr.Dropdown.update(value=cur.name, choices=[x.name for x in self.imageboardList]),
                    cur.type, cur.name, cur.mainLink, cur.user['login'], 
                    cur.user['login'] if cur.user!=None else None, cur.user['apiKey'] if cur.user!=None else None]

        self.deleteImageboardButton.click(
            fn=deleteImageboard, 
            inputs=[imageboard, self.imageboardTypeList, self.selectImageboard,self.imageboardName,self.imageboardMainLink, self.imageboardUsername, self.imageobardApiKey], 
            outputs=[imageboard, self.imageboardTypeList, self.selectImageboard,self.imageboardName,self.imageboardMainLink, self.imageboardUsername, self.imageobardApiKey]
        )

        def updateImageboard(imageboard, type, imageboardList, name, mainLink, username: str, apiKey):
            newImgboard = factoryDict[type](name, mainLink, login=username, apiKey=apiKey)
            i = 0
            for ind in range(len(self.imageboardList)):
                if (self.imageboardList[ind].name == imageboard.name):
                    i = ind
                    break 
            self.imageboardList.insert(i, newImgboard)
            self.imageboardList.pop(i+1)
            ConfigManager.saveImageboardsToJson('imagebords.json', self.imageboardList)
            return [newImgboard, gr.Dropdown.update(value=self.imageboardList[i].name, choices=[x.name for x in self.imageboardList])]

        self.saveImageboardsButton.click(
            fn=updateImageboard, inputs=[imageboard, self.imageboardTypeList, self.selectImageboard,self.imageboardName,self.imageboardMainLink, self.imageboardUsername, self.imageobardApiKey],
            outputs=[imageboard, self.selectImageboard]
        )  