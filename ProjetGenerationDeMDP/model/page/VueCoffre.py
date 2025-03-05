import os
import re
import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

from ProjetGenerationDeMDP.modelDao.SiteDao import SiteDao
from ProjetGenerationDeMDP.modelDao.UtilisateurDao import UtilisateurDao

from ProjetGenerationDeMDP.model.Chiffrement import Chiffrement
from ProjetGenerationDeMDP.model.Utilisateur import Utilisateur
from ProjetGenerationDeMDP.modelDao.MotDePasseDao import MotDePasseDao

class VueCoffre:
    """Vue pour le coffre-fort de mots de passe"""
    def __init__(self, parent, controleur):
        self.utilisateur = self._init_utilisateur()
        self.parent = parent
        self.controleur = controleur

        self.menu = None
        self.configurer_interface()

    def _init_utilisateur(self) -> Utilisateur:
        identifiant = os.getenv("login")
        mot_de_passe = os.getenv("mdp")
        return Utilisateur(identifiant, mot_de_passe)

    def configurer_interface(self):
        self.effacer()

        # Titre
        etiquette_titre = tk.Label(self.parent, text="Coffre de mot de passe", font=("Arial", 14))
        etiquette_titre.pack(pady=10)

        # Configuration de l'arborescence
        colonnes = ("Mot de passe", "Site", "Categorie", "NbCaractère", "NbChiffre",
                    "NbCaraSpe", "NbCarMini", "NbCarMaj")
        self.arborescence = ttk.Treeview(self.parent, columns=colonnes, show="headings")

        for col in colonnes:
            self.arborescence.heading(col, text=col)
            self.arborescence.column(col, anchor="center")

        # Barre de défilement
        barre_defilement = ttk.Scrollbar(self.parent, orient="vertical", command=self.arborescence.yview)
        self.arborescence.configure(yscrollcommand=barre_defilement.set)

        # Placement
        self.arborescence.pack(side="left", fill="both", expand=True)
        barre_defilement.pack(side="right", fill="y")

        # Detecte le click droit
        self.arborescence.bind("<Button-3>", self.afficher_menu)

    def effacer(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def mettre_a_jour_arborescence(self, donnees: List[Tuple]):
        for ligne in self.arborescence.get_children():
            self.arborescence.delete(ligne)
        for ligne in donnees:
            self.arborescence.insert("", "end", values=ligne)

    def afficher_menu(self, event):
        # Identifier la ligne et la colonne sur lesquelles le clic droit a eu lieu
        row = self.arborescence.identify_row(event.y)
        col = self.arborescence.identify_column(event.x)

        if not row or not col:
            return

        # Sauvegarde des informations sur la cellule ciblée
        self.clic_droit_row = row
        self.clic_droit_col = col

        # Création du menu contextuel
        self.menu = tk.Menu(self.parent, tearoff=0)
        col_index = int(col[1:]) - 1
        if col_index == 0  or col_index == 1 or col_index == 2 :
            self.menu.add_command(label="Modifier la cellule", command=lambda: self.modifier_cellule(row, col))
            self.menu.add_command(label="Supprimer la ligne", command=lambda: self.supprimer_ligne(row))
        else :
            self.menu.add_command(label="Supprimer la ligne", command=lambda: self.supprimer_ligne(row))
        self.menu.post(event.x_root, event.y_root)

        # Cacher le menu lorsque un clic est détecté ailleurs
        self.parent.bind("<Button-1>", self.cacher_menu)

    def modifier_cellule(self, row, col):
        # Détermine l'indice de la colonne
        col_index = int(col[1:]) - 1
        print(col_index)

        match col_index:
            case 0:
                col_nom = "mdp"
            case 1:
                col_nom = "idSite"
            case 2:
                col_nom = "categorie"
            case 3:
                col_nom = "nbCaractere"
            case 4:
                col_nom = "nbNum"
            case 5:
                col_nom = "nbCarSpe"
            case 6:
                col_nom = "nbCarMini"
            case 7:
                col_nom = "nbCarMaj"

        print(col_nom)
        # Récupère la valeur actuelle
        current_values = self.arborescence.item(row, "values")
        current_text = current_values[col_index]

        # Récupère la position et la taille de la cellule
        x, y, width, height = self.arborescence.bbox(row, col)

        # Création du widget Entry positionné sur la cellule
        entry = tk.Entry(self.arborescence)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, current_text)
        entry.focus()

        # Lier la touche Entrée pour sauvegarder la modification
        entry.bind("<Return>", lambda e: self.save_edit(row, col_index, col_nom, entry))
        # Détruire l'Entry en cas de perte de focus
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def save_edit(self, row, col_index, col_nom,entry):
        new_text = entry.get()
        print("nb_caractère apres",new_text)
        current_values = list(self.arborescence.item(row, "values"))
        valeur = self.arborescence.item(row, "values")
        chifr = Chiffrement()
        mdp_dao = MotDePasseDao()
        user_daod = UtilisateurDao()
        site_dao = SiteDao()
        _id = user_daod.recup_id_utilisateur(self.utilisateur.get_login())
        mdp = "\\x" + chifr.crypte_mdp(valeur[0]).hex()
        id_site = site_dao.recup_id_site(valeur[1])
        if valeur[2] == "None":
            categorie = None
        else:
            categorie = valeur[2]
        nb_caractere = int(valeur[3])
        print("nb_caractère avant",nb_caractere)
        nb_chiffre = int(valeur[4])
        nb_car_spe = int(valeur[5])
        nb_car_mini = int(valeur[6])
        nb_car_maj = int(valeur[7])
        if col_nom=="mdp":
            #Compte le nombre de caractère dans le nouveau mot de passe
            new_nb_car = len(new_text)
            mdp_dao.update_nb_caractere(new_nb_car, nb_caractere, nb_chiffre, nb_car_spe, id_site, mdp, categorie, _id, nb_car_mini, nb_car_maj)

            #Compte le nombre de caractères spéciaux dans le nouveau mot de passe
            new_nb_car_spe = len(re.sub('[\w]+' ,'', new_text))
            mdp_dao.update_nb_car_spe(new_nb_car_spe, new_nb_car, nb_chiffre, nb_car_spe, id_site, mdp, categorie, _id, nb_car_mini, nb_car_maj)

            #Compte le nombre de chiffre dans le nouveau mot de passe
            new_nb_num = len(re.sub("[^0-9]", "", new_text))
            mdp_dao.update_nb_num(new_nb_num, new_nb_car, nb_chiffre, new_nb_car_spe, id_site, mdp, categorie, _id, nb_car_mini, nb_car_maj)

            #Compte le nombre de caractère minuscule dans le nouveau mot de passe
            new_car_mini = len(re.findall(r'[a-z]',new_text))
            mdp_dao.update_mdp_car_mini(new_car_mini, new_nb_car, new_nb_num, new_nb_car_spe, id_site, mdp, categorie, _id, nb_car_mini, nb_car_maj)

            #Compte le nombre de caractère majuscule dans le nouveau mot de passe
            new_car_maj = len(re.findall(r'[A-Z]',new_text))
            mdp_dao.update_mdp_car_maj(new_car_maj, new_nb_car, new_nb_num, new_nb_car_spe, id_site, mdp, categorie, _id, new_car_mini, nb_car_maj)

            #Insere finalement le mot de passe
            mdp_dao.update_mdp("\\x" + chifr.crypte_mdp(new_text).hex(), new_nb_car, new_nb_num, new_nb_car_spe, id_site, mdp, categorie, _id, new_car_mini, new_car_maj)

        if col_nom=="categorie":
            mdp_dao.update_mdp_categorie(new_text, nb_caractere, nb_chiffre, nb_car_spe, id_site, mdp, categorie, _id, nb_car_mini, nb_car_maj)

        if col_nom=="idSite":
            verif = site_dao.verif_site(new_text)
            if(verif):
                recup = site_dao.recup_id_site(new_text)
                mdp_dao.update_site(recup, nb_caractere, nb_chiffre, nb_car_spe, id_site, mdp, categorie, _id, nb_car_mini, nb_car_maj)
            else :
                site_dao.insert_site(new_text)
                recup = site_dao.recup_id_site(new_text)
                mdp_dao.update_site(recup, nb_caractere, nb_chiffre, nb_car_spe, id_site, mdp, categorie, _id, nb_car_mini, nb_car_maj)

        current_values[col_index] = new_text
        self.arborescence.item(row, values=current_values)
        entry.destroy()

    # Marche pas tres bien, ne pas abuser du click gauche
    def cacher_menu(self, event):
        if self.menu:
            self.menu.unpost()
            self.menu = None
        self.parent.unbind_all("<Button-1>")

    def supprimer_ligne(self, row):
        valeur = self.arborescence.item(row, "values")
        chifr = Chiffrement()
        mdp_dao = MotDePasseDao()
        user_daod = UtilisateurDao()
        site_dao = SiteDao()
        _id = user_daod.recup_id_utilisateur(self.utilisateur.get_login())
        mdp = "\\x"+chifr.crypte_mdp(valeur[0]).hex()
        id_site = site_dao.recup_id_site(valeur[1])
        if valeur[2]=="None":
            categorie = None
        else :
            categorie = valeur[2]
        nb_caractere = int(valeur[3])
        nb_chiffre = int(valeur[4])
        nb_car_spe = int(valeur[5])
        nb_car_mini = int(valeur[6])
        nb_car_maj = int(valeur[7])

        mdp_dao.sup_un_mdp_selon_users(nb_caractere, nb_chiffre, nb_car_spe, id_site, mdp, categorie, _id, nb_car_mini, nb_car_maj)
        self.arborescence.delete(row)
