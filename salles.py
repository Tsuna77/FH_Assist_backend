
from secret import GOOGLE_API_KEY
from logger import rootLogger
from bdd import fh_bdd
from core import send_resp, valid_google_oauth_token, connect_from_header_connection
import mysql.connector
from mysql.connector import errorcode

import json

# dépendance au moteur API falcon
import falcon


class fh_salles():
    token = None
    db = None
    CLIENT_ID = GOOGLE_API_KEY

    def __init__(self):
        rootLogger.debug("Initialisation de l'api fh_salles")
        self.db = fh_bdd()

    def on_get(self, req, resp):
        """Recuperation de la liste des salles
        ---
            description: Recuperation de la liste des salles
            responses:
                200:
                    description: Recuperation de la liste des salles
                    schema: ResponseSchema
                401:
                    description: Erreur de token
                    schema: ResponseSchema
        """
        rootLogger.info("Appel de la commande GET de l'api fh_salles sans paramètre")
        try:
            user = connect_from_header_connection(req, resp, self.db)

        except Exception as e:
            rootLogger.error(str(e))
            send_resp(resp, falcon.HTTP_401, 401, "error", str(e))
            return
        rootLogger.debug(
            "Récupération des informations des salles en base")
        salles = self.db.list_salles()
        salle = {}
        salle['salles'] = {}
        rootLogger.debug(salles)
        for key, value in salles.items():
            rootLogger.debug(key+"=>"+str(value))
            salle['salles'][key]={}
            salle['salles'][key]['levels']=value
        send_resp(resp, falcon.HTTP_200, 200, 'salles', salle)
