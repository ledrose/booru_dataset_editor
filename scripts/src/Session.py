from pypac.parser import PACFile
from pypac import PACSession
from requests.sessions import Session
from pathlib import Path
def getSession(useProxy=True):
    # file = Path(__file__).resolve().parent / 'proxy-ssl.js'
    # print(file)
    if (useProxy):
        try:
            with open('extensions/sd-webui-boorugrabber/proxy-ssl.js') as f:
                pac = PACFile(f.read())
            session = PACSession(pac)
        except:
            print('falling back to default session')
            session = Session()
    else:
        session = requests.session()
    session.headers.update({'user-agent':'ledrose_scrapper/0.0.1'})
    return session

    