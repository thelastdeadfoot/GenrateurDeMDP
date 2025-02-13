import base64
import io
import os
import threading

import pandas as pd
import psycopg2

from ProjetGenerationDeMDP.chiffrementMDP.Chiffrement import Chiffrement
from ProjetGenerationDeMDP.model.Motdepasse import Motdepasse
from ProjetGenerationDeMDP.model.Utilisateur import Utilisateur
from ProjetGenerationDeMDP.modelDao.SiteDao import SiteDao
from ProjetGenerationDeMDP.modelDao.UtilisateurDao import UtilisateurDao


class fonctionCSV:

    def __init__(self, fichierCSV):
        self.fichierCSV = fichierCSV
        print("fonctionCSV crée")

    def pop_up(self, message, tk,duration):
        toast = tk.Toplevel()
        toast.overrideredirect(True)
        # Pour qu'il soit toujours au premier plan
        toast.attributes('-topmost', True)

        # Obtenir la position de l'écran
        screen_width = toast.winfo_screenwidth()
        screen_height = toast.winfo_screenheight()

        # La taille et la position du toast
        toast_width = 330
        toast_height = 80
        x_position = (screen_width - toast_width) // 2
        y_position = screen_height - toast_height - 50

        toast.geometry(f"{toast_width}x{toast_height}+{x_position}+{y_position}")

        # C'est pour mettre le message
        label = tk.Label(toast, text=message, bg="white", fg="black", padx=10, pady=5)
        label.pack(expand=True, fill='both')

        # Fermer la popup apres la fin du temps
        toast.after(duration, toast.destroy)

        return toast

    # La fonction qui permet d'inserer les données dans la base de données
    def load_data(self, tk,lectureDataFrame, nomTable, nomDonnee):
        # connexion a la base de données
        # probleme, ne marche qu'avec un reseau en IPv6 (on va gentiment ignorer ce probleme...)
        con = psycopg2.connect(
            "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
        cursor = con.cursor()
        try:
            print("Début de la phase d'insertion dans la base de donnée")
            csv_buffer = io.StringIO()
            lectureDataFrame.to_csv(csv_buffer, index=False, header=False)
            csv_buffer.seek(0)
            # Requete qui permet d'inserer tout les données avec un csv
            copySql = f'COPY "{nomTable}"({nomDonnee}) FROM STDOUT WITH CSV'
            cursor.copy_expert(copySql, csv_buffer)
            con.commit()
            print("Nbre de lignes enregistrés {}".format(cursor.rowcount))
            #popup qui montre que le mdp a bien été envoyée, je le decrypte avant de lui envoyée
            #je suis obliger de faire une copy de mon dataFrame, car sinon, mes element se modifie et se decrypte definitivement
            chifr = Chiffrement()
            copyDf = lectureDataFrame.copy()
            print(copyDf["mdp"])
            copyDf["mdp"] = copyDf["mdp"].apply(lambda detruit: detruit[2:])
            print(copyDf["mdp"])
            copyDf["mdp"] = copyDf["mdp"].apply(lambda decrypt: chifr.decrypteMDP(bytes.fromhex(decrypt)))
            print(copyDf["mdp"])
            self.pop_up(f"{copyDf['mdp'].iloc[0]}\nà bien été envoyée vers la base de données ✅", tk, 2000)
        except Exception as e:
            print("Une erreur est survenue pendant la phase d'insertion {}".format(e))
        finally:
            cursor.close()
            con.close()
            print("Fermeture de la connexion")

    def load_data_thread(self, df, tk, nomTable, nomDonee):
        thread = threading.Thread(target=self.load_data, args=(tk, df, nomTable, nomDonee))
        thread.start()

    #Tout la manipulation du fichier csv
    def extraction(self, NomFichier, tk, cadre_contenu):
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

        frame = tk.Frame(cadre_contenu, borderwidth=2, relief="ridge")
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        for i in range(3):
            frame.columnconfigure(i, weight=1)

        #ici, il y a "categorie", c'est un peu le else du if juste au dessus
        df.columns = ["mdp", "idSite","categorie"]

        #pour l'interface graphique
        for index, row in df.iterrows():
            print("la, on est rentré dans le for")
            ligne_df = pd.DataFrame([row])
            print(ligne_df)
            leTexte = "\n".join(ligne_df.apply(lambda row: f"{row['mdp']} / {row['idSite']}", axis=1))
            tk.Label(frame, text=leTexte, relief="solid", background="lightblue").grid(row=index+1, column=0, padx=1, pady=3, sticky="nsew")

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

        #ça aussi, pour l'interface graphique
        for index, row in df.iterrows():
            print("la, on est rentré dans le for")
            ligne_df = pd.DataFrame([row])
            print(ligne_df)
            leTexteRobuste = "\n".join(ligne_df.apply(lambda row: f"{row['Robustesse']}", axis=1))
            tk.Label(frame, text=leTexteRobuste, relief="solid", background="lightgreen").grid(row=index+1, column=1, padx=1, pady=3, sticky="nsew")

        #cela verfie si le site que l'utilisateur a mis existe
        for verifSite in df["idSite"]:
            if not site.verifSite(verifSite):
                site.insertSite(verifSite)
        # et si il existe, il recupere l'identifiant du site et le met dans la colonne idSite crée auparavant
        df["idSite"] = df["idSite"].apply(lambda site_id: site.recupIdSite(site_id))
        print(user.getLogin())
        df["idUtilisateur"] = userDao.recupIdUtilisateur(user.getLogin())
        print(df["idUtilisateur"])
        #df["idUtilisateur"] = 125

        hexConvert = df["mdp"].apply(lambda crytp : chifr.crypteMDP(crytp).hex())
        df["mdp"] = "\\x" + hexConvert
        print(df.to_string(max_rows=20))

        tk.Button(frame, text=f"Envoyer MDP", command=lambda ligne=ligne_df: self.load_data_thread(df, tk,"MotDePasse",'"mdp", "idSite", "categorie", "nbCaractere", "nbNum", "nbCarSpe", "idUtilisateur", "Robustesse", "carMini", "carMaj"')).grid(row=0, column=1, padx=1, pady=3, sticky="nsew")

        for index, row in df.iterrows():
            print("la, on est rentré dans le for")
            ligne_df = pd.DataFrame([row])
            print(ligne_df)
            tk.Button(frame, text=f"Envoyer MDP (Ligne {index})", command=lambda ligne=ligne_df: self.load_data_thread(ligne, tk,"MotDePasse",'"mdp", "idSite", "categorie", "nbCaractere", "nbNum", "nbCarSpe", "idUtilisateur", "Robustesse", "carMini", "carMaj"')).grid(row=index+1, column=2, padx=1, pady=3, sticky="nsew")
        return df

    def envoieMdpViaCSV(self, tk, cadre_contenu):
        # fait tout les modif, extrait le contenue du csv, le modifie, et l'envoie vers la bdd
        self.extraction(self.fichierCSV, tk, cadre_contenu)
