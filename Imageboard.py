import requests
from requests.auth import HTTPBasicAuth
from Image import Image
def defaultInputTransform(searchInput):
    return searchInput.replace(' ', '+')


class Imageboard:
    def __init__(self, name, mainLink, inputTransform = defaultInputTransform, login=None, apiKey=None):
        self.name = name
        self.mainLink = mainLink
        self.authLink= mainLink + '/profile.json'
        self.postLink= mainLink + '/posts.json'
        self.isAuthenticated = False
        self.user = None
        if (login!=None and apiKey!=None):
            self.user = {'login': login, 'apiKey': apiKey}
        self.inputTransform = inputTransform
    
    def requestImageSearch(self, searchInput: str):
        searcgInput = self.inputTransform(searchInput)
        postsUrl = self.mainLink+'/posts.json'
        if (not self.isAuthenticated and self.user!=None):
            self.requestAuth()
        payload = {"tags":searchInput}
        response = requests.get(postsUrl, params=payload)
        if (response.status_code==200):
            data = response.json()
            imgList = []
            for img in data:
                imgList.append(Image(
                    id=img['id'], 
                    imgLink=img['file_url'], 
                    tags=img['tag_string'].split(' '), 
                    previewImagelink=img['preview_file_url'], 
                    fullImageLink=img['file_url']
                ))
            return imgList
        else:
            raise Exception("Search was not succesful")

    def requestAuth(self):
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
    print(images[1].imgLink)

if __name__ == "__main__":
    main()