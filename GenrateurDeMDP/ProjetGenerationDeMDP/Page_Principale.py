import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from typing import List, Tuple

from ProjetGenerationDeMDP.model.FonctionCsv import FonctionCsv
from ProjetGenerationDeMDP.modelDao.SiteDao import SiteDao
from ProjetGenerationDeMDP.modelDao.UtilisateurDao import UtilisateurDao

from ProjetGenerationDeMDP.model.Chiffrement import Chiffrement
from model.Utilisateur import Utilisateur
from modelDao.MotDePasseDao import MotDePasseDao
from model.Motdepasse import Motdepasse

class ControleurGestionnaireMDP:
    """Contrôleur principal de l'application"""

    def __init__(self, root):
        self.utilisateur = self._init_utilisateur()
        self.root = root
        self.chiffrement = Chiffrement()
        self.mdp_dao = MotDePasseDao()

        # Configuration du cadre principal
        self.cadre_principal = ttk.Frame(root, padding=10)
        self.cadre_principal.pack(fill="both", expand=True)
        self.cadre_principal.config(relief="groove", borderwidth=2)

        # Menu
        self.cadre_menu = ttk.Frame(self.cadre_principal)
        self.cadre_menu.pack(fill="x", pady=5)

        # Cadre de contenu
        self.cadre_contenu = ttk.Frame(self.cadre_principal, relief="groove", borderwidth=2)
        self.cadre_contenu.pack(fill="both", expand=True, pady=10)

        # Initialisation des vues
        self.vue_generateur = VueGenerateur(self.cadre_contenu, self)
        self.vue_coffre = VueCoffre(self.cadre_contenu, self)
        self.vue_csv = VueCSV(self.cadre_contenu)

        # Configuration des boutons du menu
        self.configurer_menu()

        # Affichage initial
        self.afficher_generateur()

    def _init_utilisateur(self) -> Utilisateur:
        identifiant = os.getenv("login")
        mot_de_passe = os.getenv("mdp")
        return Utilisateur(identifiant, mot_de_passe)

    def configurer_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        file_menu.add_command(label='Coffre de mot de passe', command=self.afficher_coffre)
        file_menu.add_command(label='Generer un mot de passe', command=self.afficher_generateur)
        file_menu.add_command(label='Importer un mdp via un CSV', command=self.afficher_csv)
        file_menu.add_separator()

        def destruction():
            #ouais c'est bizzare et moche, mais c'est pour eviter l'erreur de l'import circulaire
            from logpage import LoginSystem
            self.cadre_principal.destroy()
            file_menu.destroy()
            menubar.destroy()
            LoginSystem(self.root)

        file_menu.add_command(label='Deconnexion', command=lambda: destruction())

        menubar.add_cascade(
            label="Menu",
            menu=file_menu
        )

    def afficher_generateur(self):
        self.vue_generateur = VueGenerateur(self.cadre_contenu, self)

    def afficher_coffre(self):
        self.vue_coffre = VueCoffre(self.cadre_contenu, self)
        self.mettre_a_jour_donnees_coffre()

    def afficher_csv(self):
        self.vue_csv = VueCSV(self.cadre_contenu)

    def ecrire_mot_de_passe(self):
        # Demander à l'utilisateur d'entrer un mot de passe
        mdp = simpledialog.askstring("Mot de passe", "Entrez votre mot de passe:", show="*")

        if mdp:
            try:
                # Créer un nouvel objet Motdepasse avec le mot de passe entré
                self.mot_de_passe_courant = Motdepasse(0, 0, 0, 0, 1, mdp)

                # Calculer la force du mot de passe
                force = (self.mot_de_passe_courant.verifier_robustesse_mdp() / 17) * 100
                self.vue_generateur.mettre_a_jour_barre_progression(force)

                # Mettre à jour l'affichage
                texte_resultat = f"Mot de passe : {self.mot_de_passe_courant.mdp}\n note du mot de passe : {force}"
                self.vue_generateur.etiquette_resultat.config(text=texte_resultat)

                # Activer les boutons
                self.vue_generateur.bouton_copier.config(state="normal")
                self.vue_generateur.bouton_ameliorer.config(state="normal")
                self.vue_generateur.bouton_sauvegarder.config(state="normal")

            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

    def generer_mot_de_passe(self):
        try:
            valeurs = self.vue_generateur.obtenir_valeurs_champs()
            cases_cochees = self.vue_generateur.obtenir_valeurs_cases()
            caracteres_exclus = self.vue_generateur.obtenir_caracteres_exclus()

            # Création de l'objet mot de passe
            obj_mdp = Motdepasse(valeurs['maj'], valeurs['min'],
                                 valeurs['num'], valeurs['special'], 1, None)

            if cases_cochees.get('aleatoire', False):
                print("alea")
                obj_mdp.genere_mot_de_passe(4, 4, 4, 4)

            obj_mdp.caracteres_exclus(caracteres_exclus)

            # Applique le remplacement des caractères similaires si la case est cochée
            if cases_cochees.get('remplacer_caracteres', False):
                obj_mdp.remplacer_caracteres_repetes()

            # Calcul de la force du mot de passe
            force = (obj_mdp.verifier_robustesse_mdp() / 17) * 100
            self.vue_generateur.mettre_a_jour_barre_progression(force)

            texte_resultat = f"Mot de passe : {obj_mdp.mdp}\n note du mot de passe : {force}"
            self.vue_generateur.etiquette_resultat.config(text=texte_resultat)

            # Activer les boutons de copie et d'amélioration
            self.vue_generateur.bouton_copier.config(state="normal")
            self.vue_generateur.bouton_ameliorer.config(state="normal")
            self.vue_generateur.bouton_sauvegarder.config(state="normal")
            # Stocker le mot de passe pour une éventuelle amélioration
            self.mot_de_passe_courant = obj_mdp

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides dans tous les champs")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

    def ameliorer_mot_de_passe(self):
        try:
            # Vérifier si un mot de passe a été généré
            if not hasattr(self, 'mot_de_passe_courant'):
                messagebox.showerror("Erreur", "Générez d'abord un mot de passe")
                return

            # Améliorer le mot de passe
            self.mot_de_passe_courant.upgrade_mot_de_passe()

            # Recalculer la force
            force = (self.mot_de_passe_courant.verifier_robustesse_mdp() / 17) * 100

            # Mettre à jour l'affichage
            texte_resultat = f"Mot de passe : {self.mot_de_passe_courant.mdp}\n note du mot de passe : {force}"
            self.vue_generateur.etiquette_resultat.config(text=texte_resultat)

            # Mettre à jour la barre de progression
            self.vue_generateur.mettre_a_jour_barre_progression(force)

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'améliorer le mot de passe : {str(e)}")

    def copier_mot_de_passe(self):
        try:
            mot_de_passe = self.vue_generateur.etiquette_resultat.cget("text").split("\n")[0].replace("Mot de passe : ",
                                                                                                      "")
            self.root.clipboard_clear()
            self.root.clipboard_append(mot_de_passe)
            self.root.update()
            messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papiers !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de copier : {str(e)}")

    def fenetre_sauvgarder_mot_de_passe(self):

        dialog = tk.Toplevel(self.root)
        dialog.title("Informations du mot de passe")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(dialog, text="Site:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        site_entry = tk.Entry(dialog, width=25)
        site_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(dialog, text="Catégorie:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        categorie_entry = tk.Entry(dialog, width=25)
        categorie_entry.grid(row=1, column=1, padx=10, pady=10)

        def sauvegarder():
            site = site_entry.get()
            categorie = categorie_entry.get()
            dao_util = UtilisateurDao()
            dao_site = SiteDao()
            chifr = Chiffrement()
            if not site or not categorie:
                messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
                return

            try:
                self.mot_de_passe_courant.categorie = categorie
                self.mot_de_passe_courant.site = site
                self.mdp_dao.insert_mdp(
                    nbCaractere=self.mot_de_passe_courant.taille,
                    nbNum=self.mot_de_passe_courant.nb_numero,
                    nbCarSpe=self.mot_de_passe_courant.nb_caratere_special,
                    idSite=dao_site.recup_id_site(self.mot_de_passe_courant.site),
                    mdp= "\\x"+chifr.crypte_mdp(self.mot_de_passe_courant.mdp).hex(),
                    categorie=self.mot_de_passe_courant.categorie,
                    idUtilisateur=dao_util.recup_id_utilisateur(self.utilisateur.get_login()),
                    Robuste=self.mot_de_passe_courant.verifier_robustesse_mdp(),
                    carMini=self.mot_de_passe_courant.nb_caratere_min,
                    carMaj=self.mot_de_passe_courant.nb_caratere_maj
                )
                print("nom du mot de passse")
                print(self.mot_de_passe_courant.mdp)
                messagebox.showinfo("Succès", "Mot de passe sauvegardé dans la base de données !")
                dialog.destroy()  # Fermer la fenêtre de dialogue
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder : {str(e)}")

        # Boutons pour confirmer ou annuler
        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Sauvegarder", command=sauvegarder).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Annuler", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def mettre_a_jour_donnees_coffre(self):
        mots_de_passe = self.mdp_dao.recup_all_mdp_user(self.utilisateur.get_login(), self.utilisateur.get_mdp())
        donnees_formatees = self._formater_donnees_coffre(mots_de_passe)
        self.vue_coffre.mettre_a_jour_arborescence(donnees_formatees)

    def _formater_donnees_coffre(self, donnees: List[Tuple]) -> List[Tuple]:
        donnees_formatees = []
        dao = SiteDao()
        for ligne in donnees:
            try:
                mdp_dechiffre = self.chiffrement.decrypte_mdp(ligne[0])
                transform_site = dao.recup_nom_site(ligne[1])
                cate = ligne[2]
                nbcar = ligne[3]
                nbnum = ligne[4]
                nbcarspe = ligne[5]
                nbcarmini = ligne[6]
                nbcarmaj = ligne[7]
                donnees_formatees.append((mdp_dechiffre,transform_site, cate, nbcar, nbnum, nbcarspe, nbcarmini, nbcarmaj) + ligne[1:])
            except Exception as e:
                print(f"Erreur de formatage : {e}")
                donnees_formatees.append(("ERREUR",) + ligne[1:])
        return donnees_formatees

    def executer(self):
        self.root.mainloop()

class VueGenerateur:
    """Vue pour le générateur de mot de passe"""

    def __init__(self, parent, controleur):
        self.rouge_horizontal_tpgressbar = "rouge.Horizontal.TProgressbar"
        self.parent = parent
        self.controleur = controleur
        self.champs = {}
        self.cases_a_cocher = {}
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configurer_interface()

    def ajuster_scroll(self, event):
        """Ajuste la région de défilement du canvas en fonction du contenu."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def configurer_interface(self):
        self.effacer()

        # Titre
        self.etiquette_titre = tk.Label(self.parent, text="Générateur de mot de passe", font=("Arial", 14))
        self.etiquette_titre.pack(pady=10)

        # Pour la barre de scroll
        cadre_principal = ttk.Frame(self.parent)
        cadre_principal.pack(fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(cadre_principal, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(cadre_principal, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.canvas.yview)

        self.frame_contenu = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame_contenu, anchor="center")

        def update_canvas(event):
            self.canvas.itemconfig(self.canvas_frame, width=event.width)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind("<Configure>", update_canvas)

        # Cadre pour les entrées
        cadre_entrees = ttk.Frame(self.frame_contenu)
        cadre_entrees.pack(pady=10)

        # Configuration des entrées
        config_champs = [
            ("maj", "Nombre de caractères majuscules", 0, 0),
            ("min", "Nombre de caractères minuscules", 0, 1),
            ("num", "Nombre de Numéro", 1, 0),
            ("special", "Nombre de caractères spéciaux", 1, 1)
        ]

        for cle, etiquette, ligne, colonne in config_champs:
            cadre = ttk.Frame(cadre_entrees)
            cadre.grid(row=ligne, column=colonne, padx=10, pady=5)
            tk.Label(cadre, text=etiquette).pack()
            champ = ttk.Entry(cadre, width=10)
            champ.insert("end", "0")
            champ.pack()
            self.champs[cle] = champ

        # Barre de progression
        self.barre_progression = ttk.Progressbar(
            self.frame_contenu,
            style=self.rouge_horizontal_tpgressbar,
            orient="horizontal",
            length=200,
            mode="determinate"
        )
        self.barre_progression.pack(pady=20)

        # Étiquette résultat
        self.etiquette_resultat = tk.Label(self.frame_contenu, text="", font=("Arial", 12), fg="black")
        self.etiquette_resultat.pack(pady=10)

        # Configuration des cases à cocher
        cadre_cases = ttk.Frame(self.frame_contenu)
        cadre_cases.pack(pady=5)

        config_cases = [
            ("remplacer_caracteres", "remplacer caracteres repetes", 0, 0),
            ("aleatoire", "cree un mot de passe aleatoire", 0, 1),
            ("semblable", "remplacer caractères semblable", 0, 2)
        ]

        for cle, texte, ligne, colonne in config_cases:
            var = tk.BooleanVar()
            if cle == "aleatoire":
                case = ttk.Checkbutton(cadre_cases, text=texte, variable=var, command=self.basculer_config_champs)
            else:
                case = ttk.Checkbutton(cadre_cases, text=texte, variable=var)
            case.grid(row=ligne, column=colonne, padx=5, pady=2, sticky="w")
            self.cases_a_cocher[cle] = var

        # Ajout du champ pour les caractères exclus
        cadre_exclus = ttk.Frame(self.frame_contenu)
        cadre_exclus.pack(pady=5)
        tk.Label(cadre_exclus, text="Caractères exclus").pack()
        self.champ_exclus = ttk.Entry(cadre_exclus, width=30)
        self.champ_exclus.pack()

        # Boutons
        self.bouton_generer = ttk.Button(
            self.frame_contenu,
            text="Générer le mot de passe",
            command=self.controleur.generer_mot_de_passe
        )
        self.bouton_generer.pack(pady=5)

        # Nouveau bouton pour écrire un mot de passe
        self.bouton_ecrire = ttk.Button(
            self.frame_contenu,
            text="Écrire un mot de passe",
            command=self.controleur.ecrire_mot_de_passe
        )
        self.bouton_ecrire.pack(pady=5)

        # Bouton améliorer
        self.bouton_ameliorer = ttk.Button(
            self.frame_contenu,
            text="Améliorer le mot de passe",
            command=self.controleur.ameliorer_mot_de_passe,
            state="disabled"  # Désactivé par défaut
        )
        self.bouton_ameliorer.pack(pady=5)

        self.bouton_copier = ttk.Button(
            self.frame_contenu,
            text="Copier le mot de passe",
            command=self.controleur.copier_mot_de_passe,
            state="disabled"
        )
        self.bouton_copier.pack(pady=5)

        self.bouton_sauvegarder = ttk.Button(
            self.parent,
            text="Sauvegarder le mot de passe",
            command=self.controleur.fenetre_sauvgarder_mot_de_passe,
            state="disabled"
        )
        self.bouton_sauvegarder.pack(pady=5)

    def basculer_config_champs(self):
        """
        Désactive ou active les champs de configuration
        lorsque la case 'aléatoire' est cochée
        """
        est_aleatoire = self.cases_a_cocher['aleatoire'].get()

        # Désactiver/activer les champs de configuration
        for champ in self.champs.values():
            if est_aleatoire:
                champ.config(state='disabled')
                # Mettre à 4 les valeurs quand aléatoire est coché
                champ.delete(0, tk.END)
                champ.insert(0, "4")
            else:
                champ.config(state='normal')
                # Remettre à 0 si on décoche aléatoire
                champ.delete(0, tk.END)
                champ.insert(0, "0")

    def effacer(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def obtenir_valeurs_champs(self) -> dict:
        return {cle: int(champ.get()) for cle, champ in self.champs.items()}

    def obtenir_valeurs_cases(self) -> dict:
        return {cle: var.get() for cle, var in self.cases_a_cocher.items()}

    def obtenir_caracteres_exclus(self) -> str:
        return self.champ_exclus.get()

    def mettre_a_jour_barre_progression(self, valeur: float):
        self.barre_progression["value"] = valeur
        if valeur < 30:
            self.style.configure( self.rouge_horizontal_tpgressbar, foreground='red', background='red')
        elif valeur < 65:
            self.style.configure( self.rouge_horizontal_tpgressbar, foreground='yellow', background='yellow')
        else:
            self.style.configure( self.rouge_horizontal_tpgressbar, foreground='Green', background='Green')


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

class VueCSV:
    """Vue pour l'import de CSV"""
    def __init__(self, cadre_contenu):
        self.cadre_contenu = cadre_contenu
        self.configurer_interface()

    def configurer_interface(self):
        self.effacer()

        # Titre
        etiquette_titre = tk.Label(self.cadre_contenu, text="Importer des mdp avec un CSV", font=("Arial", 14))
        etiquette_titre.pack(pady=10)

        csv_select = tk.Label(self.cadre_contenu, text="Import CSV", font=("Arial", 9))
        csv_select.pack(pady=10)

        import_bouton = ttk.Button(self.cadre_contenu, text="importer un fichier CSV", command=lambda: self.manip_csv(csv_select, tk, self.cadre_contenu))
        import_bouton.pack(pady=10)

    def effacer(self):
        for widget in self.cadre_contenu.winfo_children():
            widget.destroy()

    def manip_csv(self, label, tk, cadre_contenu):
        filename = filedialog.askopenfilename()
        print('Selectionner:', filename)
        label.config(text=filename)
        f_csv = FonctionCsv(filename)
        f_csv.envoie_mdp_via_csv(tk, cadre_contenu)

if __name__ == "__main__":
    #j'ai mis une fenetre au cas ou tu passe pas par logpage.py pour voir le resultat de ton code
    root = tk.Tk()
    root.title("Gestionnaire de mot de passe")
    root.attributes("-zoomed", True)
    root.resizable(True, True)
    app = ControleurGestionnaireMDP(root)
    app.executer()
