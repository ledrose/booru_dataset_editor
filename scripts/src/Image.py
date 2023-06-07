import requests
import pathlib
from PIL import Image as PILImage


class ImageInfoStruct():
    def __init__(self, hash, height, width, create_date, id, tag_character, tag_artist, tag_general, score, ext, general_link, preview_link):
        self.hash = hash
        self.height = height
        self.width = width
        self.create_date = create_date
        self.id = id
        self.tag_character = tag_artist
        self.tag_artist = tag_artist
        self.tag_general = tag_general
        self.ext = ext
        self.general_link = general_link
        self.preview_link = preview_link

class Image:
    def __init__(self, session, imageboardName: str, info: type(ImageInfoStruct)) -> None:
        self.imageboardName = imageboardName
        self.session = session
        self.info = info
        self.fullName = f"{info.hash}.{info.ext}"
        self.downloadName = info.hash
        self.localFile = None
        self.tags = info.tag_general
        

    def getImageTuple(self) -> tuple[str, str]:
        if self.localFile==None:
            return (self.getImageObject(), self.fullName)
        else:
            return (self.localFile, self.fullName)

    def getImageObject(self):
        print(self.info.general_link)
        try:
            bytes = self.session.get(self.info.preview_link, stream=True).raw
            img = PILImage.open(bytes)
        except:
            bytes = self.session.get(self.info.general_link, stream=True).raw
            img = PILImage.open(bytes)
        print(img)
        return img

    def saveImageWithTags(self, path: str) -> None:
        folder = pathlib.Path(path)
        if (not folder.is_dir()):
            folder.mkdir()
            
        response = self.session.get(self.info.general_link)
        if (response.status_code!=requests.codes.ok):
            raise Exception("Failed to download image")
        imgFile = folder / f'{self.downloadName}.{self.info.ext}'
        imgFile.touch(exist_ok=True)
        print("Downloaded image")
        with open(imgFile,'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

        textFile = folder / f"{self.downloadName}.txt"
        textFile.touch(exist_ok=True)
        textFile.write_text(' '.join(self.tags).replace('_', ' '))

    def tagsReplace(self, replaceDict: dict):
        tagsjoined = "'''".join(self.tags)
        for key,value in replaceDict.items():
            tagsjoined = tagsjoined.replace(key, value)
        self.tags = list(set(tagsjoined.split("'''")))


    def tagsAdd(self, addList: list):
        self.tags.extend([tag for tag in addList if tag not in self.tags])

    def tagsRemove(self, removeList: list):
        self.tags = [tag for tag in self.tags if tag not in removeList]