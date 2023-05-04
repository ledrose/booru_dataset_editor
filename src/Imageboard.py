import requests
from collections.abc import Callable
from requests.auth import HTTPBasicAuth
from src.Image import Image

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
        if (login!=None and apiKey!=None):
            self.user = {'login': login, 'apiKey': apiKey}
        self.inputTransform = inputTransform
        self.imgList = []

    def requestImageSearch(self, searchInput: str, pageNum: int = 1, imgCount: int = 20) -> list[type(Image)]:
        searcgInput = self.inputTransform(searchInput)
        postsUrl = self.mainLink+'/posts.json'
        if (not self.isAuthenticated and self.user!=None):
            self.requestAuth()
        payload = {"tags":searchInput, "page": pageNum, "limit": imgCount}
        response = requests.get(postsUrl, params=payload)
        if (response.status_code==200):
            data = response.json()
            imgList = []
            for img in data:
                try:
                    imgList.append(Image(
                        imageboardName=self.name,
                        name=img['md5'],
                        ext=img['file_ext'],
                        imgLink=img['file_url'], 
                        tags=img['tag_string'].split(' '), 
                        previewImagelink=img['preview_file_url'],
                    ))
                except:
                    print("Image with id {} can't be parsed".format(str(img['id'])))
            self.imgList = imgList
            return imgList
        else:
            raise Exception("Search was not succesful")

    def getImageLinks(self) -> list[tuple[str, str]]:
        return [x.getImageTuple() for x in self.imgList]

    def getImageWithName(self,fullName: str) -> type(Image):
        return next(x for x in self.imgList if x.fullName==fullName)

    def requestAuth(self) -> None:
        if (self.user==None):
            return Exception("User info is missing")
        basicAuth =  HTTPBasicAuth(self.user['login'], self.user['apiKey'])
        response = requests.get(self.authLink,auth=basicAuth)
        if (response.status_code==requests.codes.ok):
            if (response.json()['name']!=self.user['login']):
                print("How?")
        else:
            raise Exception("Auth is not succesful")


def main():
    iboard = Imageboard("TestBooru", "https://testbooru.donmai.us",login="ledrose", apiKey="GoS7hezv4reRL92oU4R2fLuu")
    images = iboard.requestImageSearch("1girl 1boy")
    images[1].saveImageWithTags('./testFolder')

if __name__ == "__main__":
    main()