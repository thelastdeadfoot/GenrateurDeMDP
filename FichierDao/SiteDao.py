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
    def insertSite(self, nomSite):
        print("Insertion d'une donnée site : "+ nomSite)
        data = {"nomSite" : nomSite}
        response = supabase.table("Site").insert(data).execute()
        print(response.data)
        return response.data
    
    # Insert un liste de site
    def insertSiteList(self, data):
        print("Insertion des données site")
        response = supabase.table("Site").upsert(data).execute()
        print(response.data)
        return response.data
    
    # Recupere tout les site
    def recupAllSite(self):
        print("Récupération des données site")
        response = supabase.table("Site").select("*").execute()
        print(response.data)
        return response.data
    
    # Recupere un site
    def recupOneSite(self, siteAchercher):
        print("Récupération des données de "+ siteAchercher)
        response = supabase.table("Site").select("nomSite").eq("nomSite", siteAchercher).execute()
        print(response.data)
        return response.data
    
    # Met a jour un site
    def updateSite(self, siteAmodifier, siteModifier):
        print("Mise à jour de la donnée site : "+siteAmodifier)
        response = supabase.table("Site").update({"nomSite": siteModifier}).eq("nomSite", siteAmodifier).execute()
        print(response.data)
        return response.data
    
    # Supprime un site (marche avec une liste)
    def supSite(self, siteAsup):
        print("Suppression des données site")
        response = supabase.table("Site").delete().in_("nomSite", siteAsup).execute()
        print(response.data) 
        return response.data 