import hashlib
import os
import tkinter as tk
from tkinter import messagebox

from ProjetGenerationDeMDP.model.ControleurGestionnaireMDP import ControleurGestionnaireMDP
from ProjetGenerationDeMDP.modelDao.UtilisateurDao import UtilisateurDao

class create_root:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestionnaire de mot de passe")
        self.root.attributes("-zoomed", True)
        self.root.resizable(True, True)
        LoginSystem(self.root)

class LoginSystem:
    def __init__(self, root):
        self.attempts = 0
        self.lock_time = 120
        self.utilisateur_dao = UtilisateurDao()
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        """Configuration de l'interface utilisateur"""

        self.frame_form = tk.Frame(self.root)

        label_title = tk.Label(self.frame_form, text="Connexion", font=("Arial", 16))
        label_title.pack(pady=10)

        self.frame_form.pack(pady=10)

        ligne_username = tk.Frame(self.frame_form)
        ligne_username.pack(fill="x", padx=5, pady=5)
        tk.Label(ligne_username, text="Nom d'utilisateur").pack(side="left")
        self.entry_username = tk.Entry(ligne_username)
        self.entry_username.pack(side="right", fill="x", expand=True)

        ligne_password = tk.Frame(self.frame_form)
        ligne_password.pack(fill="x", padx=5, pady=5)
        tk.Label(ligne_password, text="Mot de passe").pack(side="left")
        self.entry_password = tk.Entry(ligne_password, show="*")
        self.entry_password.pack(side="right", fill="x", expand=True)

        self.button_login = tk.Button(self.frame_form, text="Se connecter", command=self.login)
        self.button_login.pack(pady=10)

        self.button_signup = tk.Button(self.frame_form, text="Créer un compte", command=self.signup)
        self.button_signup.pack(pady=10)

    def login(self):
        """Fonction de connexion utilisant le DAO"""
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        #Hachage du mdp pour la sécuriter
        pwd_hacher = hashlib.md5(password.encode())
        print(pwd_hacher.hexdigest())

        # Vérification de l'utilisateur via le DAO
        verif = self.utilisateur_dao.verif_user(username, pwd_hacher.hexdigest())
        if verif:
            #crée les variales utilisateur pour pouvoir les récuperer par la suite
            os.environ["login"] = username
            os.environ["mdp"] = pwd_hacher.hexdigest()

            #Pour aller vers la page principal
            self.frame_form.destroy()
            ControleurGestionnaireMDP(self.root)
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
        self.frame_form.destroy()
        SignupWindow(self.root, self.utilisateur_dao)

class SignupWindow:
    def __init__(self, root, utilisateur_dao):
        self.root = root
        self.utilisateur_dao = utilisateur_dao
        self.setup_ui()

    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.frame_form = tk.Frame(self.root)
        self.frame_form.pack(pady=10)

        tk.Label(self.frame_form, text="Création du compte", font=("Arial", 16)).pack(pady=10)

        row_username = tk.Frame(self.frame_form)
        row_username.pack(fill="x", padx=5, pady=5)
        tk.Label(row_username, text="Nom d'utilisateur").pack(side="left")
        self.entry_username = tk.Entry(row_username)
        self.entry_username.pack(side="right", fill="x", expand=True)

        row_password = tk.Frame(self.frame_form)
        row_password.pack(fill="x", padx=5, pady=5)
        tk.Label(row_password, text="Mot de passe").pack(side="left")
        self.entry_password = tk.Entry(row_password, show="*")
        self.entry_password.pack(side="right", fill="x", expand=True)

        row_confirm = tk.Frame(self.frame_form)
        row_confirm.pack(fill="x", padx=5, pady=5)
        tk.Label(row_confirm, text="Confirmer le mot de passe").pack(side="left")
        self.entry_confirm_password = tk.Entry(row_confirm, show="*")
        self.entry_confirm_password.pack(side="right", fill="x", expand=True)

        tk.Button(self.frame_form, text="Créer un compte", command=self.create_account).pack(pady=10)

    def create_account(self):
        """Création d'un nouveau compte utilisateur"""
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not self.validate_inputs(username, password, confirm_password):
            return

        try:
            # Vérification si l'utilisateur existe déjà
            existing_user = self.utilisateur_dao.recup_one_user(username)
            if existing_user and len(existing_user) > 0:
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà")
                return

            # Utilisation de insertUser pour créer le nouvel utilisateur
            pwd_hacher = hashlib.md5(password.encode())
            print(pwd_hacher.hexdigest())
            result = self.utilisateur_dao.insert_user(username, pwd_hacher.hexdigest())

            if result and len(result) > 0:
                messagebox.showinfo("Succès", "Compte créé avec succès !")
                self.frame_form.destroy()
                LoginSystem(self.root)
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