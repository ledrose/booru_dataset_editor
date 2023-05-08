from .Imageboard import Imageboard
import pathlib
import json

class ConfigManager:
    @staticmethod
    def getImageboardsFromJson(filePath: str):
        with open(filePath, 'r') as f:
            config = json.load(f)
        return [Imageboard(
            name=x['name'],
            mainLink=x['mainLink'],
            login=x['user']['login'] if x['user']!=None else None,
            apiKey=x['user']['apiKey'] if x['user']!=None else None)
            for x in config]

    @staticmethod
    def saveImageboardsToJson(filePath: str, imageboardList: list[type(Imageboard)]):
        jsonList = []
        for imageboard in imageboardList:
            jsonList.append({"name":imageboard.name,
                            "mainLink":imageboard.mainLink,
                            "user": {
                                "login":imageboard.user['login'],
                                "apiKey":imageboard.user['apiKey']
                            } if imageboard.user!=None else None
                            })
        with open(filePath, "w") as f:
            f.write(json.dumps((jsonList)))