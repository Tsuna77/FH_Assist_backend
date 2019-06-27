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
from google.oauth2 import id_token
from google.auth.transport import requests
from secret import GOOGLE_API_KEY

# le reste de l'appli
from bdd import fh_bdd   # module de gestion de la base de données
from logger import rootLogger

SWAGGERUI_URL = '/swagger'
SCHEMA_URL =  '/static/v1/swagger.yaml'
STATIC_PATH = pathlib.Path(__file__).parent / 'static'

page_title = 'FH_Assist Swagger Doc'
favicon_url = 'https://funhospital.tsuna.fr/favicon.ico'


rootLogger.info("Démarrage de l'api")

def handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.body = 'Not found'


class fh_login:
  token= None
  db= None
  CLIENT_ID=GOOGLE_API_KEY

  def __init__(self):
    rootLogger.debug("Initialisation de l'api fh_login" )
    self.db = fh_bdd()

  def on_post(self,req, resp):
    rootLogger.info("Appel de la commande POST de l'api fh_login")
    response={}
    # Demande de connexion à l'application
    rootLogger.debug("Req = "+str(req))
    try:
      data = json.load(req.stream)
    except Exception as e:
      resp.status = falcon.HTTP_400
      return
    rootLogger.debug("data = "+str(data))
    try:
      google_token= data['token']
      # validation du token google
      idinfo=id_token.verify_oauth2_token(google_token, requests.Request(), self.CLIENT_ID)
      rootLogger.debug("idinfo = "+str(idinfo))
      if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
          raise ValueError('Wrong issuer.')
      userid = idinfo['sub']

      rootLogger.debug("UserData = "+str(userid))
      response['result']=u"OK"
      resp.body=json.dumps(response)
      resp.status = falcon.HTTP_200
      return
    except Exception as e:
      rootLogger.error(str(e))
      response['result']=u"KO"
      resp.body=json.dumps(response)
      resp.status = falcon.HTTP_401
      return
try:
  api = falcon.API()
  api.add_route("/connect",fh_login())
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

