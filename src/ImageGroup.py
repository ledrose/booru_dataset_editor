from src.Image import Image

class ImageGroup:
    def __init__(self, imgSet: set[type(Image)] = set()):
        self.images = imgSet

    def getGalleryTuples(self):
        x = [x.getImageTuple() for x in self.images]
        print(x)
        return x
        
    def getImageByFilename(self, filename: str) -> type(Image):
        return next((x for x in iter(self.images) if x.fullName == filename), None)

    def remove(self, img: type(Image)) -> type(Image):
        l = list(self.images)
        ind = l.index(img)
        if (img in self.images):
            self.images.remove(img)
        if ind+1 == len(l):
            return None
        return l[ind+1]

    def add(self, img: type(Image)) -> type(Image):
        self.images.add(img)
        return img

    def downloadAll(self,path: str) -> None:
        for img in self.images:
            img.saveImageWithTags(path)