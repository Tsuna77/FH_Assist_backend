#!/usr/bin/env python3
# coding: utf8

# dépendance python native
import json
import traceback
import pathlib
import sys

# dépendance au moteur API falcon
import falcon
from falcon_swagger_ui import register_swaggerui_app
# dépendance de debug
from wsgiref import simple_server

# dépendance au moteur google Oauth
from core import send_resp, valid_google_oauth_token

from hospital import fh_hospitals

# le reste de l'appli
from bdd import fh_bdd
from logger import rootLogger

SWAGGERUI_URL = '/swagger'
SCHEMA_URL = '/static/v1/swagger.yaml'
STATIC_PATH = pathlib.Path(__file__).parent / 'static'

page_title = 'FH_Assist Swagger Doc'
favicon_url = 'https://funhospital.tsuna.fr/favicon.ico'


rootLogger.info("Démarrage de l'api")




def handle_404(req, resp):
    send_resp(resp,falcon.HTTP_404,404,"error","API non trouvé")


class fh_login:
    token = None
    db = None

    def __init__(self):
        rootLogger.debug("Initialisation de l'api fh_login")
        self.db = fh_bdd()

    def on_post(self, req, resp):
        rootLogger.info("Appel de la commande POST de l'api fh_login")
        # Demande de connexion à l'application
        rootLogger.debug("Req = "+str(req))
        try:
            data = json.load(req.stream)
        except Exception as e:
            send_resp(resp,falcon.HTTP_400,400,"error","Erreur lors de l'analyse du body envoyé")
            return
        rootLogger.debug("data = "+str(data))

        try:
            idinfo= valid_google_oauth_token(data['token'])

            if not self.db.check_user_exist(idinfo['email']):
                rootLogger.info(
                    "L'utilisateur "+idinfo['email']+" n'éxiste pas encore dans la base")
                self.db.add_user(idinfo['email'])
            send_resp(resp,falcon.HTTP_200,200,"info","Token valide")
            return
        except Exception as e:
            rootLogger.error(str(e))
            send_resp(resp,falcon.HTTP_401,401,"error",str(e))
            return


try:
    api = falcon.API()
    api.add_route("/connect", fh_login())
    api.add_route("/hospitals", fh_hospitals())
    api.add_sink(handle_404, '')

    # Ajout du swagger de l'API
    api.add_static_route('/static', str(STATIC_PATH))
except Exception as e:
    rootLogger.error(str(e))
    sys.exit(1)

register_swaggerui_app(
    api, SWAGGERUI_URL, SCHEMA_URL,
    page_title=page_title,
    favicon_url=favicon_url,
    config={'supportedSubmitMethods': ['get'], }
)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
