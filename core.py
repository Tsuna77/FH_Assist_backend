import json
from secret import GOOGLE_API_KEY
from google.oauth2 import id_token
from google.auth.transport import requests
from logger import rootLogger


# dépendance au moteur API falcon
import falcon


def send_resp(resp, status, code=0, type="", message=""):
    """
        code:
          type: "integer"
          format: "int32"
        type:
          type: "string"
        message:
          type: "string"
    """
    resp.status = status
    body = {}
    body['code'] = code
    body['type'] = type
    body['message'] = message
    resp.body = json.dumps(body)


def valid_google_oauth_token(token):
    CLIENT_ID = GOOGLE_API_KEY

    google_token = token
    # validation du token google
    idinfo = id_token.verify_oauth2_token(
        google_token, requests.Request(), CLIENT_ID)
    rootLogger.debug("idinfo = "+str(idinfo))
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')
    rootLogger.info("Connexion google réussi pour "+idinfo['email'])
    return idinfo


def connect_from_header_connection(req,resp,db):
    """
    Take request
    Send email + base id
    """

    user = {}
    token = req.get_header('Authorization')
    rootLogger.debug("Token = "+str(token))
    # validation du token et récupération de l'id utilisateur
    idinfo = valid_google_oauth_token(token)
    user['email'] = idinfo['email']
    if not db.check_user_exist(user['email']):
        send_resp(resp, falcon.HTTP_401, "401", "error",
                  "Vous devez d'abord vous connecter pour créer un compte")
    user['id']=db.get_user(user['email'])
    rootLogger.debug("user = "+str(user))
    return user

