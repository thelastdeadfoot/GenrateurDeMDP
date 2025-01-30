import tkinter as tk
from tkinter import ttk, messagebox
from mot_de_passe import Motdepasse

def generer_mdp():
    try:
        mdp_obj = Motdepasse(0, 0, 0, 0, 1, "aleatoire")
        resultat_label.config(text=f"Mot de passe : {mdp_obj.mdp}")
        copie_bouton.config(state="normal")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

def copier_mdp():
    try:
        mot_de_passe = resultat_label.cget("text").replace("Mot de passe : ", "")
        fenetre.clipboard_clear()
        fenetre.clipboard_append(mot_de_passe)
        fenetre.update()
        messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papiers !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de copier : {str(e)}")

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("TitreApplication.exe")
fenetre.geometry("600x400")

# Cadre global
cadre_global = ttk.Frame(fenetre, padding=10)
cadre_global.pack(fill="both", expand=True)
cadre_global.config(relief="groove", borderwidth=2)

# Nom de l'application
titre_label = tk.Label(cadre_global, text="TitreApplication.exe", font=("Arial", 16))
titre_label.pack(fill="x", pady=5)

# Menu
menu_cadre = ttk.Frame(cadre_global)
menu_cadre.pack(fill="x", pady=5)

coffre_bouton = ttk.Button(menu_cadre, text="Coffre fort")
coffre_bouton.pack(side="left", padx=5)

generateur_bouton = ttk.Button(menu_cadre, text="Générateur de mot de passe")
generateur_bouton.pack(side="left", padx=5)

# Cadre du contenu principal
cadre_contenu = ttk.Frame(cadre_global, relief="groove", borderwidth=2)
cadre_contenu.pack(fill="both", expand=True, pady=10)

# Ajouter le contenu du générateur de mot de passe
generateur_label = tk.Label(cadre_contenu, text="Générateur de mot de passe", font=("Arial", 14))
generateur_label.pack(pady=10)

bouton_generer = ttk.Button(cadre_contenu, text="Générer le mot de passe", command=generer_mdp)
bouton_generer.pack(pady=5)

resultat_label = tk.Label(cadre_contenu, text="", font=("Arial", 12), fg="black")
resultat_label.pack(pady=10)

copie_bouton = ttk.Button(cadre_contenu, text="Copier le mot de passe", command=copier_mdp, state="disabled")
copie_bouton.pack(pady=5)

fenetre.mainloop()