class TestImage:
    def __init__(self,name):
        self.name = name

def parsePattern(str: str):
    textFrag = 'lambda ind, image: f"'
    isFirstIter = True
    while(True):
        try:
            [prekey, str] = str.split(sep='<',maxsplit=1)
            textFrag+=prekey
            [key, str] = str.split(sep='>',maxsplit=1)
            if (key=='name'):
                textFrag+='{image.name}'
            elif (key=='index'):
                textFrag+='{ind}'
            else:
                raise KeyError("Invalid pattern")
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
