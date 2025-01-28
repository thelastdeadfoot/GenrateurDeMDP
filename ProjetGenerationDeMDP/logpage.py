import os
import tkinter as tk
from tkinter import messagebox
from bcrypt import hashpw, gensalt
from supabase import create_client, Client

# Définir les clés d'environnement (faites ceci une fois, ou configurez-les dans votre système)
os.environ["SUPABASE_URL"] = "https://vijrfostiknzlxhbsgwy.supabase.co"
os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpanJmb3N0aWtuemx4aGJzZ3d5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY4NDc5NjgsImV4cCI6MjA1MjQyMzk2OH0.w3FWw1e6859mozW_I89UfxglgaEdnrIQFfnDzbCuj8g"

# Récupérer l'URL et la clé à partir des variables d'environnement
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Créer le client Supabase
supabase: Client = create_client(url, key)

# Variables pour la gestion des tentatives de connexion
attempts = 0
lock_time = 120

def login():
    """Fonction de connexion"""
    global attempts
    username = entry_username.get()
    password = entry_password.get()
    
    # Vérification dans la base de données
    response = supabase.table('users').select('*').eq('username', username).execute()
    if response.data:
        user = response.data[0]
        if hashpw(password.encode(), user['password'].encode()) == user['password'].encode():
            messagebox.showinfo("Connexion réussie", "Bienvenue!")
            reset_attempts()
            return
    # Gestion des erreurs
    attempts += 1
    if attempts >= 3:
        block_login()
    else:
        messagebox.showerror("Erreur", f"Nom d'utilisateur ou mot de passe incorrect. Tentatives restantes : {3 - attempts}")

def block_login():
    """Blocage temporaire après plusieurs tentatives échouées"""
    button_login.config(state=tk.DISABLED)
    messagebox.showwarning("Erreur", f"Trop de tentatives, nouvelles tentatives dans {lock_time} secondes.")
    root.after(lock_time * 1000, unblock_login)

def unblock_login():
    """Réactivation du bouton de connexion après le délai"""
    global attempts
    attempts = 0
    button_login.config(state=tk.NORMAL)

def reset_attempts():
    """Réinitialise le compteur de tentatives"""
    global attempts
    attempts = 0

def singup():
    """Fenêtre de création de compte"""
    def create_account():
        username = entry_username_singup.get()
        password = entry_password_singup.get()
        confirm_password = entry_confirm_password_singup.get()
        
        if not username or not password or not confirm_password:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
        
        if password != confirm_password:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return
        
        # Vérification si l'utilisateur existe déjà
        response = supabase.table('users').select('username').eq('username', username).execute()
        if response.data:
            messagebox.showerror("Erreur", "Nom d'utilisateur déjà pris.")
            return
        
        # Hachage du mot de passe et création du compte
        hashed_password = hashpw(password.encode(), gensalt())
        supabase.table('users').insert({"username": username, "password": hashed_password.decode()}).execute()
        messagebox.showinfo("Succès", "Compte créé avec succès !")
        singup_window.destroy()

    # Création de la fenêtre singup
    singup_window = tk.Tk()
    singup_window.title("Création de compte")
    singup_window.geometry("400x230")
    singup_window.resizable(False, False)

    label_title = tk.Label(singup_window, text="Création du compte", font=("Arial", 16))
    label_title.pack(pady=10)

    frame_form = tk.Frame(singup_window)
    frame_form.pack(pady=10)

    label_username = tk.Label(frame_form, text="Nom d'utilisateur")
    label_username.grid(row=0, column=0, pady=5, padx=5)
    entry_username_singup = tk.Entry(frame_form)
    entry_username_singup.grid(row=0, column=1, pady=5, padx=5)

    label_password = tk.Label(frame_form, text="Mot de passe")
    label_password.grid(row=1, column=0, pady=5, padx=5)
    entry_password_singup = tk.Entry(frame_form, show="*")
    entry_password_singup.grid(row=1, column=1, pady=5, padx=5)

    label_confirm_password = tk.Label(frame_form, text="Confirmer le mot de passe")
    label_confirm_password.grid(row=2, column=0, pady=5, padx=5)
    entry_confirm_password_singup = tk.Entry(frame_form, show="*")
    entry_confirm_password_singup.grid(row=2, column=1, pady=5, padx=5)

    button_singup = tk.Button(singup_window, text="Créer un compte", command=create_account)
    button_singup.pack(pady=10)

    singup_window.mainloop()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Page de connexion")
root.geometry("400x230")
root.resizable(False, False)

label_title = tk.Label(root, text="Connexion", font=("Arial", 16))
label_title.pack(pady=10)

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

label_username = tk.Label(frame_form, text="Nom d'utilisateur")
label_username.grid(row=0, column=0, pady=5, padx=5)
entry_username = tk.Entry(frame_form)
entry_username.grid(row=0, column=1, pady=5, padx=5)

label_password = tk.Label(frame_form, text="Mot de passe")
label_password.grid(row=1, column=0, pady=5, padx=5)
entry_password = tk.Entry(frame_form, show="*")
entry_password.grid(row=1, column=1, pady=5, padx=5)

button_login = tk.Button(root, text="Se connecter", command=login)
button_login.pack(pady=10)

button_singup = tk.Button(root, text="Créer un compte", command=singup)
button_singup.pack(pady=10)

root.mainloop()
