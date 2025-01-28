import os
import tkinter as tk
from tkinter import messagebox
from UtilisateurDao import UtilisateurDao

class LoginSystem:
    def __init__(self):
        self.attempts = 0
        self.lock_time = 120
        self.utilisateur_dao = UtilisateurDao()
        self.setup_ui()

    def login(self):
        """Fonction de connexion utilisant le DAO"""
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
            
        # Vérification de l'utilisateur via le DAO
        verif = self.utilisateur_dao.verifUser(username, password)
        
        if verif == True:
            messagebox.showinfo("Connexion réussie", "Bienvenue!")
            self.reset_attempts()
        else:
            self.handle_failed_login()

    def handle_failed_login(self):
        """Gestion des tentatives de connexion échouées"""
        self.attempts += 1
        remaining = 3 - self.attempts
        
        if self.attempts >= 3:
            self.block_login()
        else:
            messagebox.showerror("Erreur", 
                f"Nom d'utilisateur ou mot de passe incorrect. Tentatives restantes : {remaining}")

    def block_login(self):
        """Blocage temporaire après plusieurs tentatives échouées"""
        self.button_login.config(state=tk.DISABLED)
        messagebox.showwarning("Erreur", 
            f"Trop de tentatives, nouvelles tentatives dans {self.lock_time} secondes.")
        self.root.after(self.lock_time * 1000, self.unblock_login)

    def unblock_login(self):
        """Réactivation du bouton de connexion après le délai"""
        self.attempts = 0
        self.button_login.config(state=tk.NORMAL)

    def reset_attempts(self):
        """Réinitialise le compteur de tentatives"""
        self.attempts = 0

    def signup(self):
        """Fenêtre de création de compte"""
        signup_window = SignupWindow(self.utilisateur_dao)

    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.root = tk.Tk()
        self.root.title("Page de connexion")
        self.root.geometry("400x230")
        self.root.resizable(False, False)

        label_title = tk.Label(self.root, text="Connexion", font=("Arial", 16))
        label_title.pack(pady=10)

        frame_form = tk.Frame(self.root)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Nom d'utilisateur").grid(row=0, column=0, pady=5, padx=5)
        self.entry_username = tk.Entry(frame_form)
        self.entry_username.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Mot de passe").grid(row=1, column=0, pady=5, padx=5)
        self.entry_password = tk.Entry(frame_form, show="*")
        self.entry_password.grid(row=1, column=1, pady=5, padx=5)

        self.button_login = tk.Button(self.root, text="Se connecter", command=self.login)
        self.button_login.pack(pady=10)

        self.button_signup = tk.Button(self.root, text="Créer un compte", command=self.signup)
        self.button_signup.pack(pady=10)

class SignupWindow:
    def __init__(self, utilisateur_dao):
        self.utilisateur_dao = utilisateur_dao
        self.setup_ui()

    def create_account(self):
        """Création d'un nouveau compte utilisateur"""
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()
        
        if not self.validate_inputs(username, password, confirm_password):
            return
            
        try:
            # Vérification si l'utilisateur existe déjà
            existing_user = self.utilisateur_dao.recupOneUser(username)
            if existing_user and len(existing_user) > 0:
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà")
                return
                
            # Utilisation de insertUser pour créer le nouvel utilisateur
            result = self.utilisateur_dao.insertUser(username, password)
            
            if result and len(result) > 0:
                messagebox.showinfo("Succès", "Compte créé avec succès !")
                self.window.destroy()
            else:
                messagebox.showerror("Erreur", "La création du compte a échoué")
                
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def validate_inputs(self, username, password, confirm_password):
        """Validation des entrées utilisateur"""
        if not username or not password or not confirm_password:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return False
        
        if password != confirm_password:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return False
            
        return True

    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.window = tk.Toplevel()
        self.window.title("Création de compte")
        self.window.geometry("400x230")
        self.window.resizable(False, False)

        tk.Label(self.window, text="Création du compte", font=("Arial", 16)).pack(pady=10)

        frame_form = tk.Frame(self.window)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Nom d'utilisateur").grid(row=0, column=0, pady=5, padx=5)
        self.entry_username = tk.Entry(frame_form)
        self.entry_username.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Mot de passe").grid(row=1, column=0, pady=5, padx=5)
        self.entry_password = tk.Entry(frame_form, show="*")
        self.entry_password.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Confirmer le mot de passe").grid(row=2, column=0, pady=5, padx=5)
        self.entry_confirm_password = tk.Entry(frame_form, show="*")
        self.entry_confirm_password.grid(row=2, column=1, pady=5, padx=5)

        tk.Button(self.window, text="Créer un compte", command=self.create_account).pack(pady=10)

if __name__ == "__main__":
    app = LoginSystem()
    app.root.mainloop()