import requests
import pathlib

class Image:
    def __init__(self, imageboard, name, ext, imgLink, tags, previewImagelink):
        self.imageboard = imageboard
        self.imgLink = imgLink
        self.name = name
        self.ext = ext
        self.fullName = '{}.{}'.format(self.name,self.ext)
        self.tags = tags
        self.previewImageLink = previewImagelink

    def getImageTuple(self):
        return (self.previewImageLink, self.fullName)

    def saveImageWithTags(self, path):
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

        
