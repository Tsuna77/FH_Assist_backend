#!/usr/bin/env python3
# coding: utf8

import falcon
import json
import logging
import traceback


from google.oauth2 import id_token
from google.auth.transport import requests
from secret import GOOGLE_API_KEY

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.info("Démarrage de l'api")

class fh_login:
  token= None
  CLIENT_ID=GOOGLE_API_KEY

  def on_post(self,req, resp):
    response={}
    # Demande de connexion à l'application
    logging.debug("Req = "+str(req))
    try:
      data = json.load(req.stream)
    except Exception as e:
      resp.status = falcon.HTTP_400
      return
    logging.debug("data = "+str(data))
    logging.debug("Token = "+str(data['token']))
    try:
      google_token= data['token']
      # validation du token google
      idinfo=id_token.verify_oauth2_token(google_token, requests.Request(), self.CLIENT_ID)
      if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
          raise ValueError('Wrong issuer.')
      userid = idinfo['sub']

      response['result']=u"OK"
      resp.body=json.dumps(response)
      resp.status = falcon.HTTP_200
      return
    except Exception as e:
      traceback.print_exc()
      response['result']=u"KO"
      resp.body=json.dumps(response)
      resp.status = falcon.HTTP_401
      return

api = falcon.API()
api.add_route("/connect",fh_login())
