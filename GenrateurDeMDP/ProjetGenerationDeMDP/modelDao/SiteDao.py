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

class SiteDao:
    def __init__(self):
        print("Instance de SiteDao créée.")

    # Insert uniquement un site dans la bdd
    def insert_site(self, nom_site):
        print("Insertion d'une donnée site : "+ nom_site)
        data = {"nomSite" : nom_site}
        response = supabase.table("Site").insert(data).execute()
        print(response.data)
        return response.data
    
    # Insert une liste de sites
    def insert_site_list(self, data):
        print("Insertion des données site")
        response = supabase.table("Site").upsert(data).execute()
        print(response.data)
        return response.data
    
    # Recupere tout les site
    def recup_all_site(self):
        print("Récupération des données site")
        response = supabase.table("Site").select("*").execute()
        print(response.data)
        return response.data
    
    # Recupere un site
    def recup_one_site(self, site_a_chercher):
        print("Récupération des données de "+ site_a_chercher)
        response = supabase.table("Site").select("nomSite").eq("nomSite", site_a_chercher).execute()
        print(response.data)
        return response.data

    #verifie l'existence d'un site
    def verif_site(self, existe_site):
        print("verif si existe : " + existe_site)
        response = supabase.table("Site").select("nomSite").eq("nomSite", existe_site).execute()
        print(response.data)
        if response.data and len(response.data)>0:
            return True
        else :
            return False

    # Recupere l'id d'un site
    def recup_id_site(self, site_id_a_chercher):
        print("Récupération des données de " + "\'"+site_id_a_chercher+"\'")
        response = supabase.table("Site").select("idSite").eq("nomSite", site_id_a_chercher).execute()
        if response.data and len(response.data) > 0:
            e = int(response.data[0]["idSite"])
            return e

    # Met a jour un site
    def update_site(self, site_a_modifier, site_modifier):
        print("Mise à jour de la donnée site : "+site_a_modifier)
        response = supabase.table("Site").update({"nomSite": site_modifier}).eq("nomSite", site_a_modifier).execute()
        print(response.data)
        return response.data
    
    # Supprime un site (marche avec une liste)
    def sup_site(self, site_a_sup):
        print("Suppression des données site")
        response = supabase.table("Site").delete().in_("nomSite", site_a_sup).execute()
        print(response.data) 
        return response.data 