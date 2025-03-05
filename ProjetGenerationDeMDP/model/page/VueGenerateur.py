import tkinter as tk
from tkinter import ttk

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