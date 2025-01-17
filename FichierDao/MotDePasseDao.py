import os
from supabase import create_client, Client

# Définir les clés d'environnement (faites ceci une fois, ou configurez-les dans votre système)
os.environ["SUPABASE_URL"] = "https://vijrfostiknzlxhbsgwy.supabase.co"
os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpanJmb3N0aWtuemx4aGJzZ3d5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY4NDc5NjgsImV4cCI6MjA1MjQyMzk2OH0.w3FWw1e6859mozW_I89UfxglgaEdnrIQFfnDzbCuj8g"

# Récupérer l'URL et la clé à partir des variables d'environnement
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Créer le client Supabase
supabase: Client = create_client(url, key)

class MotDePasseDao:
    def __init__(self):
        print("Instance de MotDePasseDao créée.")

    # Insertion d'un seul mot de passe
    def insertMdp(self, nbCaractere, nbNum, nbCarSpe, idSite, mdp, categorie, idUtilisateur, Robuste):
        print("Insertion de donnée mdp : " +mdp)
        data = {"nbCaractere": nbCaractere, "nbNum": nbNum, "nbCarSpe": nbCarSpe, "idSite": idSite, "mdp": mdp, "categorie": categorie, "idUtilisateur" : idUtilisateur, "Robustesse": Robuste} 
        response = supabase.table("MotDePasse").insert(data).execute()
        print(response.data)
        return response.data
        
    # Insertion de mot de passe via une liste
    def insertMdpList(self, data):
        print("Insertion des données mdp")
        response = supabase.table("MotDePasse").insert(data).execute()
        #ci-dessous, permet d'inserer des elements en excluant les doublons se trouvant dans la liste
        # response = supabase.table("MotDePasse").upsert(data).execute()
        print(response.data)
        return response.data

    # Récupérer toutes les mots de passe
    def recupAllMdp(self):
        print("Récupération des données mdp")
        response = supabase.table("MotDePasse").select("*").execute()
        print(response.data)
        return response.data
        
    # Récupérer les mots de passe selon une colonne et une valeur 
    # (par exemple, pour recuperer tout les catégorie qui sont égale a "Professionnel")
    def recupMdpColonne(self, colonne, valeur):
        print("Récupération des données mdp de valeur : "+valeur+"\n colonne : "+colonne)
        response = supabase.table("MotDePasse").select("*").eq(colonne, valeur).execute()
        print(response.data)
        return response.data

    # Récupérer un mot de passe
    def recupOneMdp(self, mdpAchercher):
        print("Récupération de la donnée "+ mdpAchercher)
        response = supabase.table("MotDePasse").select("mdp").eq("mdp", mdpAchercher).execute()
        print(response.data)
        return response.data

    # Met a jour un mot de passe
    def updateMdp(self, mdpAmodifier, mdpModifier):
        print("Mise à jour de la donnée mdp : "+ mdpAmodifier)
        response = supabase.table("MotDePasse").update({"mdp": mdpModifier}).eq("mdp", mdpAmodifier).execute()
        print(response.data)
        return response.data
    
    # Met a jour la colonne du nombre de caractère d'un mot de passe donner
    def updateNbCaractere(self, mdp, nvNbCaractere):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"nbCaractere": nvNbCaractere}).eq("mdp", mdp).execute()       
        print(response.data)
        return response.data
    
    # Met a jour la colonne du nombre de de numéro d'un mot de passe donner
    def updateNbNum(self, mdp, nvNbNum):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"nbNum": nvNbNum}).eq("mdp", mdp).execute()       
        print(response.data)
        return response.data
    
    # Met a jour la colonne du nombre de caractère spéciaux d'un mot de passe donner
    def updateNbCarSpe(self, mdp, nvNbCarSpe):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"nbCarSpe": nvNbCarSpe}).eq("mdp", mdp).execute()       
        print(response.data)
        return response.data
    
    # Met a jour la colonne categorie d'un mot de passe donner
    def updateMdpCategorie(self, mdp, nvCateMdp):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"categorie": nvCateMdp}).eq("mdp", mdp).execute()       
        print(response.data)
        return response.data

    # Met a jour la colonne robuste d'un mot de passe donner
    def updateMdpRobustesse(self, mdp, nvRobMdp):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"Robustesse": nvRobMdp}).eq("mdp", mdp).execute()       
        print(response.data)
        return response.data

    # Supprimer un mot de passe (marche aussi avec une liste de mdp)
    def supMdp(self, mdpAsup):
        print("Suppression des données mdp")
        response = supabase.table("MotDePasse").delete().in_("mdp", mdpAsup).execute()
        print(response.data) 
        return response.data   

    # permet de supprimer tout les mots de passe d'un user
    # oui, je suis obliger d'utiliser une autre api pour pouvoir executer des requete en brute
    # (oui, c'est beaucoup plus chiant pour comprendre)
    # en plus on est obliger de fermer la connexion manuellement
    def supMdpSelonUsers(self, usersAsup):
        print(f"Suppression des mots de passe pour les utilisateurs : ")
        try:
            # Informations de connexion
            conn = psycopg2.connect("postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            
            # requete en dur car l'api supabase ne supporte pas les jointure dans le delete
            query = f"""
            DELETE FROM "MotDePasse"
            USING "Utilisateurs"
            WHERE "MotDePasse"."idUtilisateur" = "Utilisateurs"."idUtilisateur"
            AND "Utilisateurs"."login" IN %s;
            """
            
            cur.execute(query, (tuple(usersAsup),))
            conn.commit()
            
            print(f"Suppression réussie pour les utilisateurs : ")
        
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
        
        finally:
            if conn:
                conn.close()
                print("Connexion à la base de données fermée.")
