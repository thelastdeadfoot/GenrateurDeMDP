import os
import psycopg2
from supabase import create_client, Client

# Définition des clés d'environnement
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
    def insert_mdp(self, nbCaractere, nbNum, nbCarSpe, idSite, mdp, categorie, idUtilisateur, Robuste, carMini, carMaj):
        print("Insertion de donnée mdp : " +mdp)
        data = {"nbCaractere": nbCaractere, "nbNum": nbNum, "nbCarSpe": nbCarSpe, "idSite": idSite, "mdp": mdp, "categorie": categorie, "idUtilisateur" : idUtilisateur, "Robustesse": Robuste, "carMini" : carMini, "carMaj" : carMaj}
        response = supabase.table("MotDePasse").insert(data).execute()
        print(f"Voici le mot de passe et ses caractéristique qui vont être envoyée : {response.data}")
        return response.data
        
    # Insertion de mot de passe via une liste
    def insert_mdp_list(self, data):
        print("Insertion des données mdp")
        response = supabase.table("MotDePasse").insert(data).execute()
        #ci-dessous, permet d'inserer des elements en excluant les doublons se trouvant dans la liste
        # response = supabase.table("MotDePasse").upsert(data).execute()
        print(response.data)
        return response.data

    # Récupérer toutes les mots de passe
    def recup_all_mdp(self):
        print("Récupération des données mdp")
        response = supabase.table("MotDePasse").select("*").execute()
        print(response.data)
        return response.data

    # Récupérer les mots de passe selon une colonne et une valeur 
    # (par exemple, pour recuperer tout les catégorie qui sont égale a "Professionnel")
    def recup_mdp_colonne(self, colonne, valeur):
        print("Récupération des données mdp de valeur : "+valeur+"\n colonne : "+colonne)
        response = supabase.table("MotDePasse").select("*").eq(colonne, valeur).execute()
        print(response.data)
        return response.data

    # Récupérer un mot de passe
    def recup_one_mdp(self, mdp_a_chercher):
        print("Récupération de la donnée "+ mdp_a_chercher)
        response = supabase.table("MotDePasse").select("mdp").eq("mdp", mdp_a_chercher).execute()
        print(response.data)
        return response.data

    # Met a jour un mot de passe
    def update_mdp(self, mdp_a_modifier, mdp_modifier):
        print("Mise à jour de la donnée mdp : "+ mdp_a_modifier)
        response = supabase.table("MotDePasse").update({"mdp": mdp_modifier}).eq("mdp", mdp_a_modifier).execute()
        print(response.data)
        return response.data
    
    # Met a jour la colonne du nombre de caractère d'un mot de passe donner
    def update_nb_caractere(self, mdp, nv_nb_caractere):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"nbCaractere": nv_nb_caractere}).eq("mdp", mdp).execute()
        print(response.data)
        return response.data
    
    # Met a jour la colonne du nombre de de numéro d'un mot de passe donner
    def update_nb_num(self, mdp, nv_nb_num):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"nbNum": nv_nb_num}).eq("mdp", mdp).execute()
        print(response.data)
        return response.data
    
    # Met a jour la colonne du nombre de caractère spéciaux d'un mot de passe donner
    def update_nb_car_spe(self, mdp, nv_nb_car_spe):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"nbCarSpe": nv_nb_car_spe}).eq("mdp", mdp).execute()
        print(response.data)
        return response.data
    
    # Met a jour la colonne categorie d'un mot de passe donner
    def update_mdp_categorie(self, mdp, nv_cate_mdp):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"categorie": nv_cate_mdp}).eq("mdp", mdp).execute()
        print(response.data)
        return response.data

    # Met a jour la colonne robuste d'un mot de passe donner
    def update_mdp_robustesse(self, mdp, nv_rob_mdp):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"Robustesse": nv_rob_mdp}).eq("mdp", mdp).execute()
        print(response.data)
        return response.data
    
    # Met a jour la colonne carMini d'un mot de passe donner
    def update_mdp_car_mini(self, mdp, nv_car_mini_mdp):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"carMini": nv_car_mini_mdp}).eq("mdp", mdp).execute()
        print(response.data)
        return response.data
    
    # Met a jour la colonne carMaj d'un mot de passe donner
    def update_mdp_car_maj(self, mdp, nv_car_maj_mdp):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"carMaj": nv_car_maj_mdp}).eq("mdp", mdp).execute()
        print(response.data)
        return response.data

    # Supprimer un mot de passe (marche aussi avec une liste de mdp)
    def sup_mdp(self, mdp_a_sup):
        print("Suppression des données mdp")
        response = supabase.table("MotDePasse").delete().in_("mdp", mdp_a_sup).execute()
        print(response.data) 
        return response.data 
    
    # permet de supprimer tout les mots de passe d'un user
    # oui, je suis obliger d'utiliser une autre api pour pouvoir executer des requete en brute
    # (oui, c'est plus chiant pour comprendre)
    # en plus on est obliger de fermer la connexion manuellement
    def sup_mdp_selon_users(self, users_a_sup):
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
            
            cur.execute(query, (tuple(users_a_sup),))
            conn.commit()
            
            print(f"Suppression réussie pour les utilisateurs : ")
        
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
        
        finally:
            if conn:
                conn.close()
                print("Connexion à la base de données fermée.")

    def recup_all_mdp_user(self, login, mdp):
        print(f"Récupération des mots de passe pour l'utilisateur : {login}")

        try:
            # Connexion à la base de données
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres"
            )
            cur = conn.cursor()
            query = """
            SELECT "mdp", "idSite", "categorie", "nbCaractere", "nbNum", "nbCarSpe", "carMini", "carMaj"  
            FROM "MotDePasse"
            INNER JOIN "Utilisateurs" ON "MotDePasse"."idUtilisateur" = "Utilisateurs"."idUtilisateur"
            WHERE "Utilisateurs"."login" = %s AND "Utilisateurs"."mdpMaitre" = %s
            """
            cur.execute(query, (login, mdp))

            rows = cur.fetchall()

            cur.close()
            conn.close()

            print(f"Nombre de résultats trouvés : {len(rows)}")
            return rows

        except Exception as e:
            print(f"Erreur lors de la récupération : {e}")
            return []