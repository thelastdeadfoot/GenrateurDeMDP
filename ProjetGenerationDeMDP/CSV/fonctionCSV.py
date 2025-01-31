import os

import pandas as pd
import psycopg2

from ProjetGenerationDeMDP.chiffrementMDP.Chiffrement import Chiffrement
from ProjetGenerationDeMDP.model.Motdepasse import Motdepasse
from ProjetGenerationDeMDP.model.Utilisateur import Utilisateur
from ProjetGenerationDeMDP.modelDao.SiteDao import SiteDao
from ProjetGenerationDeMDP.modelDao.UtilisateurDao import UtilisateurDao


class fonctionCSV:
    def __init__(self):
        print("fonctionCSV crée")

    #La fonction qui permet d'inserer les données dans la base de données
    def load_data(self, lectureFichier, nomTable, nomDonnee):
        #connexion a la base de données
        #probleme, ne marche qu'avec un reseau en IPv6
        con = psycopg2.connect("postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
        cursor = con.cursor()
        try:
            print("Début de la phase d'insertion dans la base de donnée")
            #Requete qui permet d'inserer tout les données avec un csv
            copySql = f'COPY "{nomTable}"({nomDonnee}) FROM STDOUT WITH CSV'
            cursor.copy_expert(copySql, lectureFichier)
            con.commit()
            print("Nbre de lignes enregistrés {}".format(cursor.rowcount))
        except Exception  as e:
            print("Une erreur est survenue pendant la phase d'insertion {}".format(e))
        finally:
            cursor.close()
            con.close()
            print("Fermeture de la connexion")

    #Permet de copier le fichiers
    #je le fait car l'utilisateur ne veux pas que son fichier csv se fasse modifier
    def saveToFile(data):
        data.to_csv('mdpAfterChangeCSV.csv', encoding='utf-8', index=False, header=False)
        print("Le fichier a été généré avec le chemin suivant ; {}".format('mdpAfterChangeCSV.csv'))
        filesave = open('mdpAfterChangeCSV.csv', "r")
        return filesave

    #Tout la manipulation du fichier csv
    def extraction(self, NomFichier):
        #j'appelle ce qui vas me permettre de recuperer des information depuis la base de données
        mdp = Motdepasse()
        site = SiteDao()
        chifr = Chiffrement()
        userDao = UtilisateurDao()
        login = os.getenv("login")
        password = os.getenv("mdp")
        user = Utilisateur(login, password)

        #pour lire le fichier
        df = pd.read_csv(NomFichier, header=None)

        #Comme la categorie seras optionnel dans le fichiers, il faut que j'ajoute une la categorie "categorie"
        #si l'utilisateur ne met pas de categorie, je dois la combler avec un None
        nbColonnes = df.shape[1]
        if nbColonnes ==2:
            df["categorie"]=None

        #ici, il y a "categorie", c'est un peu le else du if juste au dessus
        df.columns = ["mdp", "idSite","categorie"]

        #Comme l'utilisateur mettras au moins 2 valeurs, je suis obliger de remplir a ça place les categorie qu'il a pas mis
        colonnes_manquantes = ["nbCaractere", "nbNum", "nbCarSpe", "idUtilisateur", "Robustesse","carMini","carMaj"]
        for col in colonnes_manquantes: df[col] = None

        #compte le nombre de caractère dans et le met dans la colonne nbCaractère crée auparavant
        df["nbCaractere"] = df["mdp"].str.len()

        #compte le nombre de chiffre dans le mdp et et le met dans la colonne nbNum crée auparavant
        df["nbNum"] = df["mdp"].str.count(r'\d')

        #compte le nombre de caractère spéciaux et le met dans la colonne nbCarSpe crée auparavant
        df["nbCarSpe"] = df.apply(lambda p: sum( not q.isalpha() and q.isnumeric() for q in p["mdp"] ), axis=1)

        #compte le nombre de caractère en minuscule et le met dans la colonne carMini crée auparavant
        df["carMini"] = df['mdp'].str.findall(r'[A-Z]').str.len()

        #compte le nombre caractère en majuscule et le met dans la colonne carMaj crée auparavant
        df["carMaj"] = df['mdp'].str.findall(r'[a-z]').str.len()

        #verifie la robustesse du mdp et met le resultat dans la colonne de Robustesse crée auparavant
        df["Robustesse"] = df['mdp']
        df["Robustesse"] = mdp.verifier_robustesse_mdp()

        #cela verfie si le site que l'utilisateur a mis existe
        for verifSite in df["idSite"]:
            if not site.verifSite(verifSite):
                site.insertSite(verifSite)
        # et si il existe, il recupere l'identifiant du site et le met dans la colonne idSite crée auparavant
        df["idSite"] = df["idSite"].apply(lambda site_id: site.recupIdSite(site_id))

        #df["idUtilisateur"] = userDao.recupIdUtilisateur(user.getLogin)
        df["idUtilisateur"] = 125

        hexConvert = df["mdp"].apply(lambda crytp : chifr.crypteMDP(crytp).hex())
        df["mdp"] = "\\x" + hexConvert
        print(df.to_string(max_rows=20))
        return df

    def envoieMdpViaCSV(self, fichierCSV):
        # du coup voici comment ça marche
        # fait tout les modif
        fichierTraite = self.extraction(fichierCSV)

        # puis ecrase ou crée un fichier avec toute les donnée qu'on a manipulé en format csv
        fichier = fonctionCSV.saveToFile(fichierTraite)

        # et envoie les donnée en COPY
        self.load_data(fichier, "MotDePasse",'"mdp", "idSite", "categorie", "nbCaractere", "nbNum", "nbCarSpe", "idUtilisateur", "Robustesse", "carMini", "carMaj"')

#Comment on l'utilise :
fCSV = fonctionCSV()
fCSV.envoieMdpViaCSV("mdp$.csv")