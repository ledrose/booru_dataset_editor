from src.Image import Image

class ImageGroup:
    def __init__(self, imgSet: set[type(Image)] = set()):
        self.images = imgSet

    def getGalleryTuples(self):
        return [x.getImageTuple() for x in self.images]

    def getImageByFilename(self, filename: str):
        return next((x for x in iter(self.images) if x.fullName == filename), None)

    def remove(self, img: type(Image)) -> None:
        if (img in self.images):
            self.images.remove(img)
    
    def add(self, img: type(Image)) -> None:
        self.images.add(img)

    def downloadAll(self,path: str) -> None:
        for img in self.images:
            img.saveImageWithTags(path)