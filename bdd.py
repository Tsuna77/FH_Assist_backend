import mysql.connector
from mysql.connector import errorcode
import logging

from secret import BDD_INFO


class fh_bdd:
  cnx = None

  def __new__(self):
    logging.debug("Initialisation de la classe "+self.__name__ )
    try:
      
      logging.debug("Connexion à la base...")
      self.cnx = mysql.connector.connect(**BDD_INFO)
      logging.debug("Connecté à la base...")
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.error("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logging.error("Database does not exist")
      else:
        logging.error(err)
