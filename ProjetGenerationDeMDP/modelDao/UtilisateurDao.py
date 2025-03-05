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

class UtilisateurDao:
    def __init__(self):
        print("Instance de UtilisateurDao créée.")

    # Inserer un l'utilisateur
    def insert_user(self, login, mdp):
        print("Insertion de donnée user :"+login, mdp)
        data = {"login" : login, "mdpMaitre" : mdp} 
        response = supabase.table("Utilisateurs").insert(data).execute()
        print(response.data)
        return response.data
    
    # Inserer plusieurs utilisateurs avec une liste (je pense pas que ce soit très utile du coup, mais il est la)
    def insert_user_list(self, data):
        print("Insertion des données user")
        response = supabase.table("Utilisateurs").upsert(data).execute()
        print(response.data)
        return response.data
    
    # Recuperer la liste de tout les utilisateurs
    def recup_all_user(self):
        print("Récupération des données user")
        response = supabase.table("Utilisateurs").select("*").execute()
        print(response.data)
        return response.data
    
    # Recuperer les information d'un seul utilisateur
    def recup_one_user(self, user_a_chercher):
        print("Récupération de la donnée user "+ user_a_chercher)
        response = supabase.table("Utilisateurs").select("login").eq("login", user_a_chercher).execute()
        print(response.data)
        return response.data

    # Recupere l'id d'un Utilisateur
    def recup_id_utilisateur(self, utilisateur_id_a_chercher):
        print(f"Récupération des données de '{utilisateur_id_a_chercher}'")
        response = supabase.table("Utilisateurs").select("idUtilisateur").eq("login", utilisateur_id_a_chercher).execute()
        print(response.data)
        return response.data[0]["idUtilisateur"]

    # Permet de verifier si l'utilisateur existe dans la bdd 
    # (utile lorsque il faut verifier l'existant d'un utilisateur)
    def verif_user(self, user_a_verif, user_mdp_a_verif):
        print("verif de la donnée user")
        response = supabase.table("Utilisateurs").select("login", "mdpMaitre").eq("login", user_a_verif).eq("mdpMaitre", user_mdp_a_verif).execute()
        print(response.data)
        if response.data and len(response.data)>0:
            print(True)
            return True
        else :
            print(False)
            return False
    
    # Chercher quel mot de passe est associée a un utilisateur
    def cherche_mdp_selon_user(self, user_mdp_a_chercher):
        print("Récupération de la donnée user"+ user_mdp_a_chercher)
        response = supabase.from_("Utilisateurs").select('login, MotDePasse(mdp)').eq('login', user_mdp_a_chercher).execute()
        print(response.data)
        return response.data
    
    # Mettre a jour l'identifiant de l'utilisateur
    def update_user(self, user_a_modifier, user_modifier):
        print("Mise à jour de la donnée user : "+ user_a_modifier)
        response = supabase.table("Utilisateurs").update({"login": user_modifier}).eq("login", user_a_modifier).execute()
        print(response.data)
        return response.data
    
    # Mettre a jour le mot de passe de l'utilisateur
    # On l'utiliseras si l'utilisateur veut changer de mot de passe
    def update_mdp(self, mdp_a_modifier, mdp_modifier, user):
        print("Mise à jour de la donnée user : "+ mdp_a_modifier)
        response = supabase.table("Utilisateurs").update({"mdpMaitre": mdp_modifier}).eq("mdpMaitre", mdp_a_modifier).eq("login", user).execute()
        print(response.data)
        return response.data
    
    # Supprime un utilisateur (marche seulement avec une liste)
    # je dois aussi supprimer les mots de passe qui sont associée a l'utilisateur associée
    # si tu essaye de supprimer un utilisateur qui a un mot de passe associée du 
    # gestionnaire de mot de passe, il ne vas pas le supprimer
    # il faut obligatoirement supprimer les mot de passe de l'utilisateur que tu veux supprimer avec 
    # la methode "supMdpSelonUser()" qui se trouve dans Motdepasse.py
    # avant de supprimer l'utilisateur
    def sup_user(self, user_a_sup):
        print("Suppression des données user")
        response = supabase.table("Utilisateurs").delete().in_("login", user_a_sup).execute()
        print(response.data) 
        return response.data