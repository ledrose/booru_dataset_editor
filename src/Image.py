import requests

class Image:
    def __init__(self, id, imgLink, tags, previewImagelink, fullImageLink):
        self.imgLink = imgLink
        self.id = id
        self.tags = tags
        self.previewImageLink = previewImagelink
        self.fullImageLink = fullImageLink
