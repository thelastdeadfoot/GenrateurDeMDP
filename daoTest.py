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

# Insertion de données
print("Insertion de données...")
data = {"nbCaractere": "5", "nbNum": "2", "nbCarSpe": "1", "idSite": 4, "Mdp": "2i$0o"} 
response = supabase.table("MotDePasse").insert(data).execute()
print(response.data)

# Récupérer toutes les données
print("Récupération des données...")
response = supabase.table("MotDePasse").select("*").execute()
print(response.data)

# Mettre à jour un enregistrement
print("Mise à jour des données...")
response = supabase.table("MotDePasse").update({"Mdp": "2i$00"}).eq("Mdp", "2i$0o").execute()
print(response.data)

# Supprimer un enregistrement
print("Suppression des données...")
response = supabase.table("MotDePasse").delete().eq("Mdp", "2i$00").execute()
print(response.data)