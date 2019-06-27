import mysql.connector
from mysql.connector import errorcode

from secret import BDD_INFO
from logger import rootLogger


class fh_bdd:
  cnx = None

  def __init__(self):
    rootLogger.debug("Initialisation de la classe fh_bdd" )
    try:
      
      rootLogger.debug("Connexion à la base...")
      self.cnx = mysql.connector.connect(**BDD_INFO)
      rootLogger.debug("Connecté à la base...")
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        rootLogger.error("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        rootLogger.error("Database does not exist")
      else:
        rootLogger.error(err)
