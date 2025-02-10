# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:22:46 2025

@author: Utilisateur
"""

import random
import string

liste_obj = []
"""
Attributs

categorie : Indique si le mot de passe est professionnel (booléen)
mdp : Le mot de passe lui-même (chaîne de caractères)
nb_caratere_maj : Nombre de caractères majuscules
nb_caratere_min : Nombre de caractères minuscules
nb_numero : Nombre de chiffres
nb_caratere_special : Nombre de caractères spéciaux
taille : Longueur du mot de passe

Comportement

Si mot_de_passe est None : Génère un nouveau mot de passe selon les critères spécifiés
Si mot_de_passe est un entier : Génère un mot de passe composé de mots aléatoires
Si mot_de_passe est "aleatoire" : Génère un mot de passe aléatoires (12 caratere)
Si mot_de_passe est une chaîne : Utilise cette chaîne comme mot de passe
"""

class Motdepasse :


    def __init__(self,nb_caratere_maj=0 ,nb_caratere_min=0 ,nb_numero=0 ,nb_caratere_special=0 ,professionel=0 ,mot_de_passe=None ):
        self.categorie = professionel
        
        if mot_de_passe == None:
            self.mdp = self.genere_mot_de_passe(nb_caratere_maj,nb_caratere_min,nb_numero,nb_caratere_special)
            self.mise_a_jour()
            liste_obj.append(self)
            
        
        elif type(mot_de_passe) == int:
            self.mdp = ""
            for i in range (mot_de_passe):
                mot = self.ligne_aleatoire("liste_mot.txt")
                self.mdp += mot
                self.mdp += " "
            self.mise_a_jour()
            liste_obj.append(self)
            
        elif mot_de_passe == "aleatoire":
             self.mdp = self.genere_mot_de_passe_aleatoire(12)
             self.mise_a_jour() 
             liste_obj.append(self)
             
        elif type(mot_de_passe) == str :
            self.mdp = mot_de_passe
            self.mise_a_jour() 
            liste_obj.append(self)
                    
        
             
    
    
#   Met à jour les compteurs de caractères du mot de passe actuel.
    def mise_a_jour(self):
        self.taille = len(self.mdp)
        self.nb_caratere_maj = 0
        self.nb_caratere_min = 0
        self.nb_numero = 0
        self.nb_caratere_special = 0
        for lettre in self.mdp:
                
            if 48 <= ord(lettre) <= 57 :
                self.nb_numero += 1
                
            elif 65 <= ord(lettre) <= 90 :
                self.nb_caratere_maj += 1
                
            elif 97 <= ord(lettre) <= 122 :
                self.nb_caratere_min += 1
                
            else :
                self.nb_caratere_special += 1 
                    
    def ligne_aleatoire(self ,fichier):
        try:
            with open(fichier, 'r') as f:
                lignes = f.readlines()
                if not lignes:
                    return "Erreur: Le fichier est vide"
                
                # Prend une ligne aléatoire et nettoie les espaces/retours à la ligne
                ligne_random = random.choice(lignes).strip()
                return ligne_random
        except FileNotFoundError:
            return "Erreur: Le fichier n'a pas été trouvé"
        except Exception as e:
            return f"Erreur lors de la lecture du fichier: {str(e)}"
                    
                    
                    
                    
    """
    Vérifie si le mot de passe existe dans une liste de mots de passe courants.

    Retourne : True si le mot de passe est commun, False sinon
    """
    def test_mdp_commnu(self):
        try:
            with open('mdp20000.txt', 'r') as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if ligne == self.mdp:
                        return True
                
                return False
                        
        except FileNotFoundError:
            return "Erreur: Le fichier mdp20000.txt n'a pas été trouvé"
        except Exception as e:
            return f"Erreur lors de la lecture du fichier: {str(e)}" 



    def remplacer_caracteres_repetes(self):
        for char in self.mdp:
            if self.mdp.count(char) > 2:
                liste = []
                for lettre in self.mdp:
                    liste.append(lettre)
                compteur_de_char = 0
                for i in range(len(liste)):
                    if liste[i] == char:
                        compteur_de_char += 1
                        if compteur_de_char > 2:
                            liste[i] = chr(random.randint(21, 122))
                new_de_passe =""
                for lettre in liste:
                    new_de_passe += lettre
                self.mdp = new_de_passe
        
                        
                
                
                
                
                
    def upgrade_mot_de_passe(self):
    
        self.mise_a_jour()
            
    
        if self.nb_caratere_min == 0:
            self.mdp += chr(random.randint(97, 122))  # a-z
                
    
        if self.nb_caratere_maj == 0:
            self.mdp += chr(random.randint(65, 90))   # A-Z
                
    
        if self.nb_numero == 0:
            self.mdp += chr(random.randint(48, 57))   # 0-9
                
    
        while len(self.mdp) < 12:
                
            caracteres = chr(random.randint(32, 122))
            self.mdp += random.choice(caracteres)
            
        for char in self.mdp:
            if self.mdp.count(char) > 2:
                self.remplacer_caracteres_repetes()
    
        self.mise_a_jour()
            
        return self.mdp
            
            
    """
    verifier_robustesse_mdp()
    Évalue la robustesse du mot de passe sur une échelle de 0 à 17.
    
    Critères pénalisants :
    
    Longueur insuffisante (-2 ou -6 points)
    Absence de minuscules (-2 points)
    Absence de majuscules (-2 points)
    Absence de chiffres (-1 point)
    Absence de caractères spéciaux (-2 points)
    Mot de passe commun (-3 points)
    Mot de passe déjà existant (-2 points)
    Caractères répétés (-1 point)
    """
    def verifier_robustesse_mdp(self):
        note = 17
        liste_probleme = []
        if len(self.mdp) < 8:
             note -= 4
             liste_probleme.append("beacoup trop court")
             
        if len(self.mdp) < 12:
             note -= 2
             liste_probleme.append("trop court")
             
        if self.nb_caratere_min == 0:
            note -= 2
            liste_probleme.append("pas de caratere minuscule")
            
            
            
        if self.nb_caratere_maj == 0:
            note -= 2
            liste_probleme.append("pas de caratere majuscule")
            
            
        if self.nb_numero == 0:
            note -= 1
            liste_probleme.append("pas de numero")
            
        if self.nb_caratere_special == 0:
            note -= 2
            liste_probleme.append("pas de caratere alphanumerique")
            
        if self.test_mdp_commnu() == True:
            note -= 3
            liste_probleme.append("mot de passe commun")
        
        liste_mdp =[]
        for obj in liste_obj:
            liste_mdp.append(obj.mdp)
        
        if liste_mdp.count(self.mdp) > 1:
            liste_probleme.append("mot de passe deja existant")
            note -= 2
            
        for char in self.mdp:
            if self.mdp.count(char) > 2 :
                note -= 1
                liste_probleme.append("des lettre en commun")
                break
        
        return note 

    # Calcule la complexité du mot de passe basée sur le nombre de possibilités pour chaque type de caractère.
    def complexiter(self):
        comp_nb = 10**self.nb_numero
        comp_cara_maj = 26**self.nb_caratere_maj
        comp_cara_min = 26**self.nb_caratere_min
        comp_cara_spe = 42**self.nb_caratere_special
        return comp_nb*comp_cara_maj*comp_cara_min*comp_cara_spe
    
    def genere_mot_de_passe(self,nb_caratere_maj,nb_caratere_min,nb_numero,nb_caratere_special):
        mdp = ""
        for i in range(nb_caratere_min):
            variable = random.randint(97, 122)

            variable = chr(variable)
            mdp += variable
        
        for i in range(nb_caratere_maj):
            variable = random.randint(65, 90)

            variable = chr(variable)
            mdp += variable

        for i in range(nb_numero):
            variable = random.randint(48, 57)

            variable = chr(variable)
            mdp += variable

        for i in range(nb_caratere_special):
            indice = random.randint(0, len(string.punctuation) - 1)
            variable = string.punctuation[indice]
            mdp += variable
        mdp = ''.join(random.sample(mdp,len(mdp)))
        mdp.mise_a_jour
        return mdp
    
    
    def genere_mot_de_passe_aleatoire(self,taille):
        mdp = ""
        for i in range(taille):
            variable = random.randint(32, 122)
            print(variable)
            variable = chr(variable)
            mdp += variable
        
        mdp = ''.join(random.sample(mdp,len(mdp)))
        mdp.mise_a_jour
        return mdp
