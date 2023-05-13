from .Imageboard import ImageboardFactory, Imageboard
from pypac.parser import PACFile
from pypac import PACSession
import pathlib
import requests
import json


class ConfigManager:
    @staticmethod
    def getImageboardsFromJson(filePath: str):
        with open(filePath, 'r') as f:
            config = json.load(f)
        return [ImageboardFactory.danbooruLike(
                    name=x['name'],
                    mainLink=x['mainLink'],
                    login=x['user']['login'] if x['user']!=None else None,
                    apiKey=x['user']['apiKey'] if x['user']!=None else None) if x['type']=='danbooru' else
                ImageboardFactory.derpibooruLike(
                    name=x['name'], 
                    mainLink=x['mainLink'])
            for x in config]

    @staticmethod
    def saveImageboardsToJson(filePath: str, imageboardList: list[type(Imageboard)]):
        jsonList = []
        for imageboard in imageboardList:
            jsonList.append({"name":imageboard.name,
                            "type": imageboard.type,
                            "mainLink":imageboard.mainLink,
                            "user": {
                                "login":imageboard.user['login'],
                                "apiKey":imageboard.user['apiKey']
                            } if imageboard.user!=None else None
                            })
        with open(filePath, "w") as f:
            f.write(json.dumps((jsonList)))
