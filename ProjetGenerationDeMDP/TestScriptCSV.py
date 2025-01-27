import pandas as pd
import psycopg2

def load_data(lectureFichier, nomTable, nomDonnee):
        con = psycopg2.connect("postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
        cursor = con.cursor()
        try:
            cursor = con.cursor()
            print("Début de la phase d'insertion dans la base de donnée")
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

def saveToFile(data):
    data.to_csv('mdpAfterChangeCSV.csv', encoding='utf-8', index=False, header=False)
    print("Le fichier a été généré avec le chemin suivant ; {}".format('mdpAfterChangeCSV.csv'))
    filesave = open('mdpAfterChangeCSV.csv', "r")
    return filesave

def extraction(NomFichier):
    #pour lire le fichier
    df = pd.read_csv(NomFichier, header=None)
    print(df.to_string(max_rows=20))
    return df

fichierTraite = extraction("mdp$.csv")
fichier = saveToFile(fichierTraite)
load_data(fichier, "MotDePasse", '"nbCaractere", "nbNum", "nbCarSpe", "idSite", "mdp", "categorie", "idUtilisateur", "Robustesse", "carMini", "carMaj"')