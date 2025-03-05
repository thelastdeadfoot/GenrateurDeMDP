import tkinter as tk
from tkinter import ttk, filedialog

from ProjetGenerationDeMDP.model.FonctionCsv import FonctionCsv

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