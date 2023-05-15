import requests
import pathlib
from PIL import Image as PILImage

class Image:
    def __init__(self, session, imageboardName: str, name: str, ext: str, imgLink: str, previewImagelink: str, tags: list[str] = []) -> None:
        self.imageboardName = imageboardName
        self.imgLink = imgLink
        self.name = name
        self.ext = ext
        self.fullName = f"{self.name}.{self.ext}"
        self.localFile = None
        self.tags = tags
        self.previewImageLink = previewImagelink
        self.session = session

    def getImageTuple(self) -> tuple[str, str]:
        if self.localFile==None:
            return (self.getImageObject(), self.fullName)
        else:
            return (self.localFile, self.fullName)

    def getImageObject(self):
        print(self.imgLink)
        bytes = self.session.get(self.previewImageLink, stream=True).raw
        img = PILImage.open(bytes)
        print(img)
        return img

    def saveImageWithTags(self, path: str) -> None:
        folder = pathlib.Path(path)
        if (not folder.is_dir()):
            folder.mkdir()
            
        response = self.session.get(self.imgLink)
        if (response.status_code!=requests.codes.ok):
            raise Exception("Failed to download image")
        imgFile = folder / self.fullName
        imgFile.touch(exist_ok=True)
        print("Downloaded image")
        with open(imgFile,'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

        textFile = folder / "{}.txt".format(self.name)
        textFile.touch(exist_ok=True)
        textFile.write_text(' '.join(self.tags))

        
