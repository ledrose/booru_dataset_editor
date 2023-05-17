from scripts.src.Image import Image
from scripts.src.PatternParser import parsePattern
from collections import Counter
import gradio as gr
import tqdm

class ImageGroup:
    def __init__(self, imgSet: set[type(Image)] = set()):
        self.images = imgSet
        self.filter = None

    def getGalleryTuples(self):
        return [x.getImageTuple() for x in tqdm.tqdm(self.getFilteredImgSet(), unit="images loaded", desc="Loading Images")]
        
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

    def downloadAll(self,path: str, pattern) -> None:
        pattern = parsePattern(pattern)
        for ind, img in tqdm.tqdm(enumerate(self.images)):
            img.downloadName = pattern(ind, img)
            img.saveImageWithTags(path)

    def getFilteredImgSet(self, type='AND'):
        if (self.filter==None):
            return self.images
        if type=='AND':
            return [x for x in self.images if all(tag in self.filter for tag in x.tags)]
        elif type=='OR':
            return [x for x in self.images if any(tag in self.filter for tag in x.tags)]
        else:
            raise ValueError("Incorrect type of filtration")


    def getTagsInfo(self):
        tags = []
        for image in self.images:
            tags.extend(image.tags)
        tags = Counter(tags)
        # print(tags[0])
        return [f"{x} {y}" for x,y in tags.most_common()]