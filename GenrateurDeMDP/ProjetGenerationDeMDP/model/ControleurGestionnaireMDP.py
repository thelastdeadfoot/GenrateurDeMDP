import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Tuple

from ProjetGenerationDeMDP.model.page.VueCSV import VueCSV
from ProjetGenerationDeMDP.model.page.VueCoffre import VueCoffre
from ProjetGenerationDeMDP.model.page.VueGenerateur import VueGenerateur
from ProjetGenerationDeMDP.modelDao.SiteDao import SiteDao
from ProjetGenerationDeMDP.modelDao.UtilisateurDao import UtilisateurDao

from ProjetGenerationDeMDP.model.Chiffrement import Chiffrement
from ProjetGenerationDeMDP.model.Utilisateur import Utilisateur
from ProjetGenerationDeMDP.modelDao.MotDePasseDao import MotDePasseDao
from ProjetGenerationDeMDP.model.Motdepasse import Motdepasse

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

if __name__ == "__main__":
    #j'ai mis une fenetre au cas ou tu passe pas par logpage.py pour voir le resultat de ton code
    root = tk.Tk()
    root.title("Gestionnaire de mot de passe")
    root.attributes("-zoomed", True)
    root.resizable(True, True)
    app = ControleurGestionnaireMDP(root)
    app.executer()