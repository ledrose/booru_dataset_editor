import requests
from Image import Image
def defaultInputTransform(searchInput):
    return searchInput.replace(' ', '+')


class Imageboard:
    def __init__(self, name, mainLink, inputTransform = defaultInputTransform, apiKey=None):
        self.name = name
        self.mainLink = mainLink
        self.apiKey = apiKey
        self.inputTransform = inputTransform
    
    def requestImageSearch(self, searchInput: str):
        searcgInput = self.inputTransform(searchInput)
        postsUrl = self.mainLink+'/posts.json'
        # TODO authentication
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
            return Exception("Request is not succesful")



def main():
    iboard = Imageboard("TestBooru", "https://testbooru.donmai.us/")
    images = iboard.requestImageSearch("1girl 1boy")
    print(images[1].imgLink)

if __name__ == "__main__":
    main()