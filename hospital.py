
from secret import GOOGLE_API_KEY
from logger import rootLogger
from bdd import fh_bdd
from core import send_resp, valid_google_oauth_token, connect_from_header_connection
import mysql.connector
from mysql.connector import errorcode

import json

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
        """Recuperation de la liste des hopitaux disponible
        ---
            description: Recuperation de la liste des hopitaux
            responses:
                200:
                    description: Recuperation de la liste des hopitaux
                    schema: ResponseSchema
                401:
                    description: Erreur de token
                    schema: ResponseSchema
        """
        rootLogger.info("Appel de la commande GET de l'api fh_hospitals")
        try:
            user = connect_from_header_connection(req, resp, self.db)

        except Exception as e:
            rootLogger.error(str(e))
            send_resp(resp, falcon.HTTP_401, 401, "error", str(e))
            return
        rootLogger.debug(
            "Récupération des hopitaux de l'utilisateur {!r}".format(user))
        hospitals = self.db.list_hospitals(user['id'])
        hosp = {}
        hosp['hospitals'] = []
        for hospital in hospitals:
            rootLogger.debug(hospital)
            hosp['hospitals'].append({"name": hospital[2], "id": hospital[0]})
        send_resp(resp, falcon.HTTP_200, 200, 'hospitals', hosp)

    def on_post(self, req, resp):
        """Creation d'un nouvel hopital
        ---
            description: Creation d'un nouvel hopital
            responses:
                200:
                    description: Recuperation de la liste des hopitaux
                    schema: ResponseSchema
                400:
                    description: Erreur d'analyse du body
                    schema: ResponseSchema
                401:
                    description: Erreur de token
                    schema: ResponseSchema
                409:
                    description: La ressource existe deja
                    schema: ResponseSchema
        """
        rootLogger.info("Appel de la commande POST de l'api fh_hospitals")
        try:
            user = connect_from_header_connection(req, resp, self.db)

        except Exception as e:
            rootLogger.error(str(e))
            send_resp(resp, falcon.HTTP_401, 401, "error", str(e))
            return

        try:
            data = json.load(req.stream)
        except Exception as e:
            send_resp(resp, falcon.HTTP_400, 400, "error",
                      "Erreur lors de l'analyse du body envoyé")
            return
        rootLogger.debug("data = {!r}".format(data))

        try:
            self.db.add_hospital(user['id'], data['name'])
            send_resp(resp, falcon.HTTP_201, 201, "Info",
                      "L'hopital {!s} à été créé".format(data['name']))
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                send_resp(resp, falcon.HTTP_409, 409, "error",
                          "L'hopital existe déjà")
            else:
                print(e)
                send_resp(resp, falcon.HTTP_500, 500, "error",
                          "Erreur non géré")
            return
