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
    def insertUser(self, login, mdp):
        print("Insertion de donnée user :"+login, mdp)
        data = {"login" : login, "mdpMaitre" : mdp} 
        response = supabase.table("Utilisateurs").insert(data).execute()
        print(response.data)
        return response.data
    
    # Inserer plusieurs utilisateurs avec une liste (je pense pas que ce soit très utile du coup, mais il est la)
    def insertUserList(self, data):
        print("Insertion des données user")
        response = supabase.table("Utilisateurs").upsert(data).execute()
        print(response.data)
        return response.data
    
    # Recuperer la liste de tout les utilisateurs
    def recupAllUser(self):
        print("Récupération des données user")
        response = supabase.table("Utilisateurs").select("*").execute()
        print(response.data)
        return response.data
    
    # Recuperer les information d'un seul utilisateur
    def recupOneUser(self, userAchercher):
        print("Récupération de la donnée user "+ userAchercher)
        response = supabase.table("Utilisateurs").select("login").eq("login", userAchercher).execute()
        print(response.data)
        return response.data
    
    # Chercher quel mot de passe est associée a un utilisateur
    def ChercheMdpSelonUser(self, userMdpAchercher):
        print("Récupération de la donnée user"+ userMdpAchercher)
        response = supabase.from_("Utilisateurs").select('login, MotDePasse(mdp)').eq('login', userMdpAchercher).execute()
        print(response.data)
        return response.data
    
    # Mettre a jour l'identifiant de l'utilisateur
    def updateUser(self, userAmodifier, userModifier):
        print("Mise à jour de la donnée user : "+ userAmodifier)
        response = supabase.table("Utilisateurs").update({"login": userModifier}).eq("login", userAmodifier).execute()
        print(response.data)
        return response.data
    
    # Mettre a jour le mot de passe de l'utilisateur
    # On l'utiliseras si l'utilisateur veut changer de mot de passe
    def updateMdp(self, mdpAmodifier, mdpModifier):
        print("Mise à jour de la donnée user : "+ mdpAmodifier)
        response = supabase.table("Utilisateurs").update({"mdpMaitre": mdpModifier}).eq("mdpMaitre", mdpAmodifier).execute()
        print(response.data)
        return response.data
    
    # Supprime un utilisateur (marche seulement avec des list)
    # je dois aussi supprimer les mots de passe qui sont associée a l'utilisateur associée
    # a l'heure actuelle, si tu essaye de supprimer un utilisateur qui a un mot de passe associée du 
    # gestionnaire de mot de passe, il ne vas pas le supprimer
    def supUser(self, userAsup):
        print("Suppression des données user")
        response = supabase.table("Utilisateurs").delete().in_("login", userAsup).execute()
        print(response.data) 
        return response.data