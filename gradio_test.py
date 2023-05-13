import requests
from pypac import PACSession
from pypac.parser import PACFile
from collections.abc import Callable
from requests.auth import HTTPBasicAuth
import pathlib

class Image:
    def __init__(self, imageboardName: str, name: str, ext: str, imgLink: str, previewImagelink: str, tags: list[str] = []) -> None:
        self.imageboardName = imageboardName
        self.imgLink = imgLink
        self.name = name
        self.ext = ext
        self.fullName = f"{self.name}.{self.ext}"
        self.tags = tags
        self.previewImageLink = previewImagelink

    def getImageTuple(self) -> tuple[str, str]:
        return (self.imgLink, self.fullName)

    def saveImageWithTags(self, path: str) -> None:
        folder = pathlib.Path(path)
        if (not folder.is_dir()):
            folder.mkdir()
            
        response = requests.get(self.imgLink)
        if (response.status_code!=requests.codes.ok):
            raise Exception("Failed to download image")
        imgFile = folder / self.fullName
        imgFile.touch(exist_ok=True)
        with open(imgFile,'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

        textFile = folder / "{}.txt".format(self.name)
        textFile.touch(exist_ok=True)
        textFile.write_text(' '.join(self.tags))

        
#TODO фабрика ииджбордов :Ъ
def defaultInputTransform(searchInput: str) -> str:
    return searchInput.replace(' ', '+')

class Imageboard:
    def __init__(self, name: str, mainLink: str, inputTransform: Callable[[str],str] = defaultInputTransform, login: str = None, apiKey: str = None) -> None:
        self.name = name
        self.mainLink = mainLink
        self.authLink= mainLink + '/profile.json'
        self.postLink= mainLink + '/posts.json'
        self.isAuthenticated = False
        self.user = None
        # with open('proxy-ssl.js') as f:
        #     pac = PACFile(f.read())
        self.session = requests.session()
        self.session.headers.update({'user-agent':'ledrose_scrapper/0.0.1'})
        
        if (login!=None and apiKey!=None):
            self.user = {'login': login, 'apiKey': apiKey}
        self.inputTransform = inputTransform

    def requestImageSearch(self, searchInput: str, pageNum: int = 1, imgCount: int = 20) -> set[type(Image)]:
        searchInput = self.inputTransform(searchInput)
        postsUrl = self.mainLink+'/posts.json'
        if (not self.isAuthenticated and self.user!=None):
            self.requestAuth()
        payload = {"tags":searchInput, "page": pageNum, "limit": imgCount}
        response = self.session.get(postsUrl, params=payload)
        if (response.status_code==200):
            print("Response_sc = 200")
            data = response.json()
            imgSet = set()
            for img in data:
                try:
                    print(img)
                    imgSet.add(Image(
                        imageboardName=self.name,
                        name=img['md5'],
                        ext=img['file_ext'],
                        imgLink=img['file_url'], 
                        tags=img['tag_string'].split(' '), 
                        previewImagelink=img['preview_file_url'],
                    ))
                except:
                    print("Image with id {} can't be parsed".format(str(img['id'])))
            return imgSet
        else:
            raise Exception("Search was not succesful")

    def getImageLinks(self) -> list[tuple[str, str]]:
        return [x.getImageTuple() for x in self.imgList]

    def getImageWithFilename(self,filename: str) -> type(Image):
        return next(x for x in self.imgList if x.fullName==filename)

    def requestAuth(self) -> None:
        if (self.user==None):
            return Exception("User info is missing")
        basicAuth =  HTTPBasicAuth(self.user['login'], self.user['apiKey'])
        response = self.session.get(self.authLink,auth=basicAuth)
        if (response.status_code==requests.codes.ok):
            if (response.json()['name']!=self.user['login']):
                print("How?")
        else:
            raise Exception("Auth is not succesful")


def main():
    iboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="Jrz525bCrCMYmRv57CesvybP")
    images = iboard.requestImageSearch("1girl 1boy")
    print(images)

if __name__ == "__main__":
    main()