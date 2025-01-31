import tkinter as tk
from tkinter import ttk, messagebox
from motdepasse import Motdepasse

def generer_mdp():
    try:
        # Récupération des valeurs des entrées
        nombre1 = int(entry1.get())
        nombre2 = int(entry2.get())
        nombre3 = int(entry3.get())
        nombre4 = int(entry4.get())
        
        mdp_obj = Motdepasse(nombre1, nombre2, nombre3, nombre4, 1, None)
        bar["value"] = (mdp_obj.verifier_robustesse_mdp()/17)*100
        if bar["value"] < 30:
            s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        elif bar["value"] < 65:
            s.configure("red.Horizontal.TProgressbar", foreground='yellow', background='yellow')
        else:
            s.configure("red.Horizontal.TProgressbar", foreground='Green', background='Green')
            
        # Récupération des conditions cochées
        conditions_cochees = []
        if var1.get():
            conditions_cochees.append("Condition 1")
        if var2.get():
            conditions_cochees.append("Condition 2")
        if var3.get():
            conditions_cochees.append("Condition 3")
        if var4.get():
            conditions_cochees.append("Condition 4")
        if var5.get():
            conditions_cochees.append("Condition 5")
        if var6.get(): 
            conditions_cochees.append("Condition 6")
        print(conditions_cochees)
        # Création du texte des conditions
        
        resultat_label.config(text=f"Mot de passe : {mdp_obj.mdp}\n note du mot de passe : {bar['value']}")
        copie_bouton.config(state="normal")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des nombres valides dans tous les champs")
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

# Création du cadre pour les entrées numériques
entries_frame = ttk.Frame(cadre_contenu)
entries_frame.pack(pady=10)

# Création des 4 entrées en grille 2x2
frame1 = ttk.Frame(entries_frame)
frame1.grid(row=0, column=0, padx=10, pady=5)
tk.Label(frame1, text="Nombre de caratere maluscule").pack()
entry1 = ttk.Entry(frame1, width=10)
entry1.insert("end", "0")
entry1.pack()

frame2 = ttk.Frame(entries_frame)
frame2.grid(row=0, column=1, padx=10, pady=5)
tk.Label(frame2, text="Nombre de caratere minuscule").pack()
entry2 = ttk.Entry(frame2, width=10)
entry2.insert("end", "0")
entry2.pack()

frame3 = ttk.Frame(entries_frame)
frame3.grid(row=1, column=0, padx=10, pady=5)
tk.Label(frame3, text="Nombre de Numero").pack()
entry3 = ttk.Entry(frame3, width=10)
entry3.insert("end", "0")
entry3.pack()

frame4 = ttk.Frame(entries_frame)
frame4.grid(row=1, column=1, padx=10, pady=5)
tk.Label(frame4, text="Nombre de caratere speciale").pack()
entry4 = ttk.Entry(frame4, width=10)
entry4.insert("end", "0")
entry4.pack()

bouton_generer = ttk.Button(cadre_contenu, text="Générer le mot de passe", command=generer_mdp)
bouton_generer.pack(pady=5)

s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

resultat_label = tk.Label(cadre_contenu, text="", font=("Arial", 12), fg="black")
resultat_label.pack(pady=10)

# Création du cadre pour les cases à cocher
checkbox_frame = ttk.Frame(cadre_contenu)
checkbox_frame.pack(pady=5)

# Variables pour chaque case à cocher
var1 = tk.BooleanVar()
var2 = tk.BooleanVar()
var3 = tk.BooleanVar()
var4 = tk.BooleanVar()
var5 = tk.BooleanVar()
var6 = tk.BooleanVar()

# Première rangée
checkbox1 = ttk.Checkbutton(checkbox_frame, text="Retirer les caractères semblables", variable=var1)
checkbox1.grid(row=0, column=0, padx=5, pady=2, sticky="w")

checkbox2 = ttk.Checkbutton(checkbox_frame, text="Condition 2", variable=var2)
checkbox2.grid(row=0, column=1, padx=5, pady=2, sticky="w")

checkbox3 = ttk.Checkbutton(checkbox_frame, text="Condition 3", variable=var3)
checkbox3.grid(row=0, column=2, padx=5, pady=2, sticky="w")

# Deuxième rangée
checkbox4 = ttk.Checkbutton(checkbox_frame, text="Condition 4", variable=var4)
checkbox4.grid(row=1, column=0, padx=5, pady=2, sticky="w")

checkbox5 = ttk.Checkbutton(checkbox_frame, text="Condition 5", variable=var5)
checkbox5.grid(row=1, column=1, padx=5, pady=2, sticky="w")

checkbox6 = ttk.Checkbutton(checkbox_frame, text="Condition 6", variable=var6)
checkbox6.grid(row=1, column=2, padx=5, pady=2, sticky="w")

bar = ttk.Progressbar(cadre_contenu, style="red.Horizontal.TProgressbar", orient="horizontal", length=200, mode="determinate")
bar.pack(pady=20)

copie_bouton = ttk.Button(cadre_contenu, text="Copier le mot de passe", command=copier_mdp, state="disabled")
copie_bouton.pack(pady=5)

fenetre.mainloop()
