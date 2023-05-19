class TestImage:
    def __init__(self,name):
        self.name = name

dictKeyword = {
    'hash': '{info.hash[0:50]}',
    'index': '{ind}',
    'h': '{info.height}',
    'w': '{info.width}',
    'id': '{info.id}',
    'ext': '{info.ext}',
    'tag_char': '{info.tag_character[0:50]}',
    'create_date': '{info.create_date}'
}

def parsePattern(str: str):
    textFrag = 'lambda ind, info: f"'
    isFirstIter = True
    while(True):
        try:
            [prekey, str] = str.split(sep='<',maxsplit=1)
            textFrag+=prekey
            [key, str] = str.split(sep='>',maxsplit=1)
            if (key=='hash'):
                textFrag+='{info.hash}'
            textFrag+=dictKeyword[key]
            isFirstIter=False
        except ValueError:
            if (isFirstIter):
                raise KeyError("No pattern detected")
            break
    textFrag+=(str+'"')
    return eval(textFrag)

if __name__ == '__main__':
    img = TestImage("Vasyliy")
    print(parsePattern('Hy there~~~ My number is <index> and my name is name>')(4, img))



# <index> -- 0,1,2...
# <name> -- default name (usually hash)
