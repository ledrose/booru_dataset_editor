from .Imageboard import ImageboardFactory, Imageboard, factoryDict
from pypac.parser import PACFile
from pypac import PACSession
import pathlib
import requests
import json

defaultImageboards = '[{"name": "Danbooru", "type": "danbooru", "mainLink": "https://danbooru.donmai.us", "user": null}, {"name": "Derpibooru", "type": "derpibooru", "mainLink": "https://derpibooru.org", "user": null}, {"name": "Gelbooru", "type": "gelbooru", "mainLink": "https://gelbooru.com", "user": null}, {"name": "TestBooru", "type": "danbooru", "mainLink": "https://testbooru.donmai.us/", "user": null}]'

class ConfigManager:
    @staticmethod
    def getImageboardsFromJson(filePath: str):
        try:
            with open(filePath, 'wr+') as f:
                config = json.load(f)
        except:
            config = json.loads(defaultImageboards)
        return [factoryDict[x['type']](
                    name=x['name'],
                    mainLink=x['mainLink'],
                    login=x['user']['login'] if x['user']!=None else None,
                    apiKey=x['user']['apiKey'] if x['user']!=None else None,
                    )
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
        with open(filePath, "w+") as f:
            f.write(json.dumps((jsonList)))
