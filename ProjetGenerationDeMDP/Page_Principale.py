import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Tuple

from chiffrementMDP.Chiffrement import Chiffrement
from model.Utilisateur import Utilisateur
from modelDao.MotDePasseDao import MotDePasseDao
from model.Motdepasse import Motdepasse

class VueGenerateur:
    """Vue pour le générateur de mot de passe"""
    
    def __init__(self, parent, controleur):
        self.parent = parent
        self.controleur = controleur
        self.champs = {}
        self.cases_a_cocher = {}
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configurer_interface()

    def configurer_interface(self):
        self.effacer()
        
        # Titre
        self.etiquette_titre = tk.Label(self.parent, text="Générateur de mot de passe", font=("Arial", 14))
        self.etiquette_titre.pack(pady=10)
        
        # Cadre pour les entrées
        cadre_entrees = ttk.Frame(self.parent)
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
            self.parent,
            style="rouge.Horizontal.TProgressbar",
            orient="horizontal",
            length=200,
            mode="determinate"
        )
        self.barre_progression.pack(pady=20)
        
        # Étiquette résultat
        self.etiquette_resultat = tk.Label(self.parent, text="", font=("Arial", 12), fg="black")
        self.etiquette_resultat.pack(pady=10)
        
        # Configuration des cases à cocher
        cadre_cases = ttk.Frame(self.parent)
        cadre_cases.pack(pady=5)
        
        config_cases = [
            ("remplacer_caracteres", "remplacer caracteres repetes", 0, 0),
            ("aleatoire", "cree un mot de passe aleatoire", 0, 1),
            ("cond3", "Condition 3", 0, 2),
            ("cond4", "Condition 4", 1, 0),
            ("cond5", "Condition 5", 1, 1),
            ("cond6", "Condition 6", 1, 2)
        ]
        
        for cle, texte, ligne, colonne in config_cases:
            var = tk.BooleanVar()
            if cle == "aleatoire":
                case = ttk.Checkbutton(cadre_cases, text=texte, variable=var, command=self.basculer_config_champs)
            else:
                case = ttk.Checkbutton(cadre_cases, text=texte, variable=var)
            case.grid(row=ligne, column=colonne, padx=5, pady=2, sticky="w")
            self.cases_a_cocher[cle] = var
        
        # Boutons
        self.bouton_generer = ttk.Button(
            self.parent,
            text="Générer le mot de passe",
            command=self.controleur.generer_mot_de_passe
        )
        self.bouton_generer.pack(pady=5)

        # Nouveau bouton pour écrire un mot de passe
        self.bouton_ecrire = ttk.Button(
            self.parent,
            text="Écrire un mot de passe",
            command=self.controleur.ecrire_mot_de_passe
        )
        self.bouton_ecrire.pack(pady=5)
        
        # Bouton améliorer
        self.bouton_ameliorer = ttk.Button(
            self.parent,
            text="Améliorer le mot de passe",
            command=self.controleur.ameliorer_mot_de_passe,
            state="disabled"  # Désactivé par défaut
        )
        self.bouton_ameliorer.pack(pady=5)
        
        self.bouton_copier = ttk.Button(
            self.parent,
            text="Copier le mot de passe",
            command=self.controleur.copier_mot_de_passe,
            state="disabled"
        )
        self.bouton_copier.pack(pady=5)

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

    def mettre_a_jour_barre_progression(self, valeur: float):
        self.barre_progression["value"] = valeur
        if valeur < 30:
            self.style.configure("rouge.Horizontal.TProgressbar", foreground='red', background='red')
        elif valeur < 65:
            self.style.configure("rouge.Horizontal.TProgressbar", foreground='yellow', background='yellow')
        else:
            self.style.configure("rouge.Horizontal.TProgressbar", foreground='Green', background='Green')

class ControleurGestionnaireMDP:
    """Contrôleur principal de l'application"""
    
    def __init__(self):
        self.utilisateur = self._init_utilisateur()
        self.chiffrement = Chiffrement()
        self.mdp_dao = MotDePasseDao()
        
        # Configuration de la fenêtre principale
        self.racine = tk.Tk()
        self.racine.title("Gestionnaire de mots de passe")
        self.racine.geometry("600x400")
        
        # Configuration du cadre principal
        self.cadre_principal = ttk.Frame(self.racine, padding=10)
        self.cadre_principal.pack(fill="both", expand=True)
        self.cadre_principal.config(relief="groove", borderwidth=2)
        
        # Titre de l'application
        self.titre_app = tk.Label(self.cadre_principal, text="Gestionnaire de mots de passe", font=("Arial", 16))
        self.titre_app.pack(fill="x", pady=5)
        
        # Menu
        self.cadre_menu = ttk.Frame(self.cadre_principal)
        self.cadre_menu.pack(fill="x", pady=5)
        
        # Cadre de contenu
        self.cadre_contenu = ttk.Frame(self.cadre_principal, relief="groove", borderwidth=2)
        self.cadre_contenu.pack(fill="both", expand=True, pady=10)
        
        # Initialisation des vues
        self.vue_generateur = VueGenerateur(self.cadre_contenu, self)
        self.vue_coffre = VueCoffre(self.cadre_contenu, self)
        
        # Configuration des boutons du menu
        self.configurer_menu()
        
        # Affichage initial
        self.afficher_generateur()

    def _init_utilisateur(self) -> Utilisateur:
        identifiant = os.getenv("login")
        mot_de_passe = os.getenv("mdp")
        return Utilisateur(identifiant, mot_de_passe)

    def configurer_menu(self):
        ttk.Button(self.cadre_menu, text="Coffre fort", 
                   command=self.afficher_coffre).pack(side="left", padx=5)
        ttk.Button(self.cadre_menu, text="Générateur de mot de passe", 
                   command=self.afficher_generateur).pack(side="left", padx=5)

    def afficher_generateur(self):
        self.vue_generateur = VueGenerateur(self.cadre_contenu, self)

    def afficher_coffre(self):
        self.vue_coffre = VueCoffre(self.cadre_contenu, self)
        self.mettre_a_jour_donnees_coffre()

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
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

    def generer_mot_de_passe(self):
        try:
            valeurs = self.vue_generateur.obtenir_valeurs_champs()
            cases_cochees = self.vue_generateur.obtenir_valeurs_cases()
            
            # Création de l'objet mot de passe
            obj_mdp = Motdepasse(valeurs['maj'], valeurs['min'], 
                                valeurs['num'], valeurs['special'], 1, None)
            
            # Applique le remplacement des caractères similaires si la case est cochée
            if cases_cochees.get('remplacer_caracteres', False):
                obj_mdp.remplacer_caracteres_repetes()
            
            if cases_cochees.get('aleatoire', False):
                print("alea")
                obj_mdp.genere_mot_de_passe(4, 4, 4, 4)
            
            # Calcul de la force du mot de passe
            force = (obj_mdp.verifier_robustesse_mdp() / 17) * 100
            self.vue_generateur.mettre_a_jour_barre_progression(force)
            
            texte_resultat = f"Mot de passe : {obj_mdp.mdp}\n note du mot de passe : {force}"
            self.vue_generateur.etiquette_resultat.config(text=texte_resultat)
            
            # Activer les boutons de copie et d'amélioration
            self.vue_generateur.bouton_copier.config(state="normal")
            self.vue_generateur.bouton_ameliorer.config(state="normal")
            
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
            mot_de_passe = self.vue_generateur.etiquette_resultat.cget("text").split("\n")[0].replace("Mot de passe : ", "")
            self.racine.clipboard_clear()
            self.racine.clipboard_append(mot_de_passe)
            self.racine.update()
            messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papiers !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de copier : {str(e)}")

    def mettre_a_jour_donnees_coffre(self):
        mots_de_passe = self.mdp_dao.recupAllMdpUser(self.utilisateur.getLogin(), self.utilisateur.getMdp())
        donnees_formatees = self._formater_donnees_coffre(mots_de_passe)
        self.vue_coffre.mettre_a_jour_arborescence(donnees_formatees)

    def _formater_donnees_coffre(self, donnees: List[Tuple]) -> List[Tuple]:
        donnees_formatees = []
        for ligne in donnees:
            try:
                mdp_dechiffre = self.chiffrement.decrypteMDP(ligne[0])
                donnees_formatees.append((mdp_dechiffre,) + ligne[1:])
            except Exception as e:
                print(f"Erreur de formatage : {e}")
                donnees_formatees.append(("ERREUR",) + ligne[1:])
        return donnees_formatees

    def executer(self):
        self.racine.mainloop()

class VueCoffre:
    """Vue pour le coffre-fort de mots de passe"""
    
    def __init__(self, parent, controleur):
        self.parent = parent
        self.controleur = controleur
        self.configurer_interface()

    def configurer_interface(self):
        self.effacer()
        
        # Titre
        self.etiquette_titre = tk.Label(self.parent, text="Coffre de mot de passe", font=("Arial", 14))
        self.etiquette_titre.pack(pady=10)
        
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

    def effacer(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def mettre_a_jour_arborescence(self, donnees: List[Tuple]):
        for ligne in self.arborescence.get_children():
            self.arborescence.delete(ligne)
        for ligne in donnees:
            self.arborescence.insert("", "end", values=ligne)

if __name__ == "__main__":
    app = ControleurGestionnaireMDP()
    app.executer()
