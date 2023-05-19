from scripts.src.Image import Image
from scripts.src.PatternParser import parsePattern
from collections import Counter
import gradio as gr
import tqdm

class ImageGroup:
    def __init__(self, imgSet: set[type(Image)] = set()):
        self.images = imgSet
        self.filter = None
        self.filterType = None

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
        for ind, img in tqdm.tqdm(enumerate(self.getFilteredImgSet())):
            img.downloadName = pattern(ind, img.info)
            img.saveImageWithTags(path)

    def getFilteredImgSet(self, filter=True):
        # print(f"{self.filter}  {self.filterType}")
        # print([x.tags for x in self.images])
        if filter:
            arr = []
            if self.filterType=='AND':
                for image in self.images:
                    isAll = True
                    for tag in self.filter:
                        if (not tag in image.tags):
                            isAll=False
                    if (isAll):
                        arr.append(image)
                # print(arr)
                # return [x for x in self.images if all(tag in self.filter for tag in x.tags)]
                return arr
            elif self.filterType=='OR':
                if (not self.filter):
                    return self.images
                for image in self.images:
                    isSome =False
                    for tag in self.filter:
                        if (tag in image.tags):
                            isSome=True
                    if (isSome):
                        arr.append(image)
                return arr
            # return [x for x in self.images if any(tag in self.filter for tag in x.tags)]
        return self.images

    def getTagsInfo(self, useFilter=True):
        tags = []
        for image in self.getFilteredImgSet(filter=useFilter):
            tags.extend(image.tags)
        tags = Counter(tags).most_common()
        # print(tags[0])
        return [f'{x} {y}' for x,y in tags]

    def replaceTags(self, source: str, dest: str):
        keys = [x.strip() for x in source.split(',')]
        values = [x.strip() for x in dest.split(',')]
        if (len(keys)>len(values)):
            values+=['']*(len(keys)-len(values))
        if (len(values)>len(keys)):
            keys+=['']*(len(values)-len(keys))
        replaceDict = dict([(key,val) for key, val in zip(keys, values) if (key!='' and val!='')])
        addList = [val for key,val in zip(keys,values) if (key=='' and val!='')]
        removeList = [key for key,val in zip(keys,values) if (key!='' and val=='')]
        for image in self.getFilteredImgSet():
            if (replaceDict):
                image.tagsReplace(replaceDict)
            if (addList):
                image.tagsAdd(addList)
            if (removeList):
                image.tagsRemove(removeList)