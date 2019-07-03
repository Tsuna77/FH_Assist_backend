#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dépendance python native
import json
import traceback
import pathlib
import sys
import codecs


# dépendance au moteur API falcon
import falcon
#from falcon_swagger_ui import register_swaggerui_app
from falcon_apispec import FalconPlugin
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields

# dépendance de debug
from wsgiref import simple_server

# dépendance au moteur google Oauth
from core import send_resp, valid_google_oauth_token, ResponseSchema

from hospital import fh_hospitals
from salles import fh_salles

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
    """Connection à l'api
    ---
      description: Connection à l'api

    """
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
    connect_api=fh_login()
    hospital_api=fh_hospitals()
    salles_api=fh_salles()
    api.add_route("/connect", connect_api)
    api.add_route("/hospitals", hospital_api)
    api.add_route("/salles", salles_api)
    api.add_sink(handle_404, '')

    # Ajout du swagger de l'API
    api.add_static_route(SWAGGERUI_URL, str(STATIC_PATH))
except Exception as e:
    rootLogger.error(str(e))
    sys.exit(1)

spec = APISpec(
    title='Swagger FH_assistant',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FalconPlugin(api),
        MarshmallowPlugin()
    ],
)

spec.components.schema('Response', schema=ResponseSchema)
spec.path(resource=connect_api)
spec.path(resource=hospital_api)
spec.path(resource=salles_api)
f= codecs.open(str(STATIC_PATH)+"/v1/swagger.yaml", "w", "utf-8")
f.write(spec.to_yaml())
f.close()


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
