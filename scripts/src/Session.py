from pypac.parser import PACFile
from pypac import PACSession
from requests.sessions import Session
def getSession(useProxy=True):
    if (useProxy):
        try:
            with open('proxy-ssl.js') as f:
                pac = PACFile(f.read())
            session = PACSession(pac)
        except:
            session = Session()
    else:
        session = requests.session()
    session.headers.update({'user-agent':'ledrose_scrapper/0.0.1'})
    return session