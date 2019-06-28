
from secret import GOOGLE_API_KEY
from logger import rootLogger
from bdd import fh_bdd
from core import send_resp, valid_google_oauth_token, connect_from_header_connection

# dépendance au moteur API falcon
import falcon


class fh_hospitals:
    token = None
    db = None
    CLIENT_ID = GOOGLE_API_KEY

    def __init__(self):
        rootLogger.debug("Initialisation de l'api fh_login")
        self.db = fh_bdd()

    def on_get(self, req, resp):
        rootLogger.info("Appel de la commande GET de l'api fh_hospitals")
        user=connect_from_header_connection(req,resp,self.db)
        rootLogger.debug("Récupération des hopitaux de l'utilisateur "+str(user))
        hospitals=self.db.list_hospitals(user['id']);
        hosp={}
        hosp['hospitals']=[]
        for hospital in hospitals:
            rootLogger.debug(hospital)
            hosp['hospitals'].append({"name":hospital[2],"id":hospital[0]})
        send_resp(resp,falcon.HTTP_200,200,'hospitals',hosp)

