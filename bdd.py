import mysql.connector
from mysql.connector import errorcode

from secret import BDD_INFO
from logger import rootLogger

from yoyo import read_migrations
from yoyo import get_backend

import json


class fh_bdd:
    cnx = None

    def __init__(self):
        rootLogger.debug("Initialisation de la classe fh_bdd")
        self.migration()
        try:
            rootLogger.debug("Connexion à la base...")
            self.cnx = mysql.connector.connect(**BDD_INFO)
            rootLogger.debug("Connecté à la base...")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                rootLogger.error(
                    "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                rootLogger.error("Database does not exist")
            else:
                rootLogger.error(err)
        self.cnx.autocommit = True

    def migration(self):
        rootLogger.debug("Lancement de la migration yoyo")
        backend = get_backend(
            'mysql://'+BDD_INFO['user']+':'+BDD_INFO['password']+'@'+BDD_INFO['host']+'/'+BDD_INFO['database'])
        migrations = read_migrations('sql')
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
        rootLogger.debug("migration terminée")

    def check_user_exist(self, email):
        rootLogger.debug("Test de l'existance du mail "+email)
        curseur = self.cnx.cursor()
        curseur.execute("SELECT id from FH_user where email='"+email+"'")
        result = curseur.fetchall()

        if len(result) == 0:
            rootLogger.debug("email non trouvé")
            return False
        else:
            rootLogger.debug("email trouvé")
            return True

    def add_user(self, email):
        rootLogger.debug("Création de l'utilisateur "+email)
        curseur = self.cnx.cursor()
        curseur.execute(
            "INSERT INTO `FH_user` (`id`, `email`) VALUES (NULL, '"+email+"')")

    def get_user(self, email):
        rootLogger.debug("Récupération de l'utilisateur "+email)
        curseur = self.cnx.cursor()
        curseur.execute("SELECT id from FH_user where email='"+email+"'")
        result = curseur.fetchall()
        # ligne 1, colone 1
        return result[0][0]

    def list_hospitals(self,userId):
        rootLogger.debug("Récupération des hopitaux de l'utilsateur "+str(userId))
        curseur = self.cnx.cursor()
        curseur.execute("SELECT * from FH_hospital where id_user='"+str(userId)+"'")
        result = curseur.fetchall()
        return result

    def add_hospital(self, userid, name):
        rootLogger.debug("Création de l'hopital "+name+" pour l'utilisateur "+str(userid))
        curseur = self.cnx.cursor()
        curseur.execute(
            "INSERT INTO `FH_hospital` (`id`, `id_user`, `nom`) VALUES (NULL,'"+str(userid)+"' ,%s)", (name,))

