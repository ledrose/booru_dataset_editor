import requests
from collections.abc import Callable
from requests.auth import HTTPBasicAuth
from scripts.src.Session import getSession
from scripts.src.Image import Image
import pathlib


class ImageboardFactory:

    @staticmethod
    def danbooruLike(name: str, mainLink: str, login: str = None, apiKey: str = None):
        def inputTransform(searchInput: str) -> str:
            return searchInput.replace(' ', '+')
        def parseData(json):
            return json
        def parseImage(data):
            return {
                'name':data['md5'],
                'ext':data['file_ext'],
                'imgLink':data['file_url'], 
                'tags':data['tag_string'].split(' '), 
                'previewImagelink':data['large_file_url'],
            }
        def payloadCreator(searchInput, pageNum, limit):
            return {"tags":searchInput, "page": pageNum, "limit": limit}
        return Imageboard(name=name, mainLink=mainLink, type='danbooru', inputTransform=inputTransform, parseImage=parseImage, parseData=parseData, payloadCreator=payloadCreator, isApiKeyNeeded=True, login=login, apiKey=apiKey,
                        authSublink='/profile.json', postsSublink='/posts.json')
        
    @staticmethod
    def derpibooruLike(name: str, mainLink: str, login: str = None, apiKey: str = None):
        def inputTransform(str: str) -> str:
            return str.replace('&&', 'AND').replace('||', 'OR')
        def parseData(json):
            return json['images']
        def parseImage(data):
            return {
                'name':data['sha512_hash'],
                'ext':data['format'],
                'imgLink':data['representations']['full'], 
                'tags':data['tags'], 
                'previewImagelink':data['representations']['medium'],
            }
        def payloadCreator(searchInput, pageNum, limit):
            return {"q":searchInput, "page": pageNum, "per_page": limit}
        return Imageboard(name=name, mainLink=mainLink, type='derpibooru', inputTransform=inputTransform, parseImage=parseImage, parseData=parseData, payloadCreator=payloadCreator, isApiKeyNeeded=False,
                        postsSublink='/api/v1/json/search/images')
    
    @staticmethod
    def gelbooruLike(name: str, mainLink: str, login: str = None, apiKey: str = None):
        def inputTransform(str: str) -> str:
            return str.replace(',', '+')
        def parseData(json):
            return json['post']
        def parseImage(data):
            return {
                'name':data['md5'],
                'ext':data['image'].replace(data['md5']+'.',''),
                'imgLink':data['file_url'], 
                'tags': ' '.split(data['tags']), 
                'previewImagelink':data['preview_url'],
            }
        def payloadCreator(searchInput, pageNum, limit):
            return {"tags":searchInput, "pid": pageNum, "limit": limit, 'json': 1, 'page':'dapi','s':'post','q':'index'}
        return Imageboard(name=name, mainLink=mainLink, type='gelbooru', inputTransform=inputTransform, parseImage=parseImage, parseData=parseData, payloadCreator=payloadCreator, isApiKeyNeeded=False,
                        postsSublink='/index.php?page=dapi&s=post&q=index')

factoryDict = {
    'danbooru': ImageboardFactory.danbooruLike,
    'derpibooru': ImageboardFactory.derpibooruLike,
    'gelbooru': ImageboardFactory.gelbooruLike
}        



class Imageboard:
    def __init__(self, name: str, mainLink: str, type: str,
                inputTransform: Callable[[str],str], postsSublink: str, parseData: Callable, parseImage: Callable, payloadCreator: Callable,
                isApiKeyNeeded: bool = True, authSublink: str = None, login: str = None, apiKey: str = None) -> None:
        self.name = name
        self.type = type
        self.mainLink = mainLink
        self.postLink= mainLink + postsSublink
        self.isApiKeyNeeded = isApiKeyNeeded
        self.session = None
        self.parseData = parseData
        self.parseImage = parseImage
        self.payloadCreator = payloadCreator
        self.allowedExt = {'jpg','png','gif'}
        
        if (isApiKeyNeeded):
            self.authLink= mainLink + authSublink
            self.isAuthenticated = False
            self.user = None
            if (login!=None and apiKey!=None):
                if (login.strip()!='' and apiKey.strip()!=''):
                    self.user = {'login': login, 'apiKey': apiKey}
        else:
            self.isAuthenticated = True
            self.user = None
        self.inputTransform = inputTransform

    def requestImageSearch(self, searchInput: str, pageNum: int = 1, imgCount: int = 20) -> set[type(Image)]:
        if (self.session==None):
            self.session = getSession()
        searchInput = self.inputTransform(searchInput)
        if (not self.isAuthenticated and self.user!=None):
            self.requestAuth()
        response = self.session.get(self.postLink, params=self.payloadCreator(searchInput, pageNum, imgCount))
        if (response.status_code==200):
            data = response.json()
            # print(data)
            imgSet = set()
            for img in self.parseData(data):
                try:
                    img = self.parseImage(img)
                    print(img)
                    if (not img['ext'] in self.allowedExt):
                        raise ConnectionError("Not supported format")
                    imgSet.add(Image(
                        session = self.session,
                        imageboardName=self.name,
                        name=img['name'],
                        ext=img['ext'],
                        imgLink=img['imgLink'], 
                        tags=img['tags'], 
                        previewImagelink=img['previewImagelink'],
                    ))
                except:
                    print("Image can't be parsed")
            return imgSet
        else:
            raise Exception("Search was not succesful")

    def getImageLinks(self) -> list[tuple[str, str]]:
        return [x.getImageTuple() for x in self.imgList]

    def getImageWithFilename(self,filename: str) -> type(Image):
        return next(x for x in self.imgList if x.fullName==filename)

    def requestAuth(self) -> None:
        if (self.authLink==None):
            return Exception("Authentication is not supported on this type of Imageboard")
        if (self.user==None):
            return Exception("User info is missing")
        basicAuth =  HTTPBasicAuth(self.user['login'], self.user['apiKey'])
        response = self.session.get(self.authLink,auth=basicAuth)
        if (response.status_code!=requests.codes.ok):
            raise Exception("Auth is not succesful")


def main():
    iboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="Jrz525bCrCMYmRv57CesvybP")
    images = iboard.requestImageSearch("1girl 1boy")
    print(images)
    images[1].saveImageWithTags('./testFolder')

if __name__ == "__main__":
    main()