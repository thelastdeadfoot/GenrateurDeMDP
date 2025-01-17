# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:22:46 2025

@author: Utilisateur
"""

import random
import string
class Mot_de_passe :

    


    def __init__(self,nb_caratere_maj,nb_caratere_min,nb_numero,nb_caratere_special,mot_de_passe=None):
        
        
        if mot_de_passe == None:
            self.taille = nb_caratere_maj + nb_caratere_min + nb_numero + nb_caratere_special
            self.mdp = self.genere_mot_de_passe(nb_caratere_maj,nb_caratere_min,nb_numero,nb_caratere_special)
            self.nb_caratere_maj = nb_caratere_maj
            self.nb_caratere_min = nb_caratere_min
            self.nb_numero = nb_numero
            self.nb_caratere_special = nb_caratere_special
        
        elif type(mot_de_passe) == int:
            self.mdp = ""
            for i in range (mot_de_passe):
                mot = self.ligne_aleatoire("liste_mot.txt")
                self.mdp += mot
                self.mdp += " "
            self.mise_a_jour()
                
        
        else :
            self.mdp = mot_de_passe
            self.taille = len(mot_de_passe)
            self.nb_caratere_maj = 0
            self.nb_caratere_min = 0
            self.nb_numero = 0
            self.nb_caratere_special = 0
            for lettre in mot_de_passe:
                    
                if 48 <= ord(lettre) <= 57 :
                    self.nb_numero += 1
                    
                elif 65 <= ord(lettre) <= 90 :
                    self.nb_caratere_maj += 1
                    
                elif 97 <= ord(lettre) <= 122 :
                    self.nb_caratere_min += 1
                    
                else :
                    self.nb_caratere_special += 1    
                    
                    
                    
    def mise_a_jour(self):
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
            with open(fichier, 'r', encoding='utf-8') as f:
                # Convertit le fichier en liste de lignes
                lignes = f.readlines()
                
                # Vérifie si le fichier n'est pas vide
                if not lignes:
                    return "Erreur: Le fichier est vide"
                
                # Prend une ligne aléatoire et nettoie les espaces/retours à la ligne
                ligne_random = random.choice(lignes).strip()
                return ligne_random
        except FileNotFoundError:
            return "Erreur: Le fichier n'a pas été trouvé"
        except Exception as e:
            return f"Erreur lors de la lecture du fichier: {str(e)}"
                    
                    
                    
                    
    
    def comparer(self):
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
                
            caracteres = chr(random.randint(21, 122))
            self.mdp += random.choice(caracteres)
            
        for char in self.mdp:
            if self.mdp.count(char) > 2:
                self.remplacer_caracteres_repetes()
    
        self.mise_a_jour()
            
        return self.mdp
            
            
    def verifier_robustesse_mdp(self):
        note = 12
        liste_probleme = []
        if len(self.get_mdp()) < 8:
             note -= 4
             liste_probleme.append("beacoup trop court")
             
        if len(self.get_mdp()) < 12:
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
            
        if self.comparer() == True:
            note -= 3
            liste_probleme.append("mot de passe commun")
            
        for char in self.mdp:
            if self.mdp.count(char) > 2 :
                note -= 1
                liste_probleme.append("des lettre en commun")
                break
        
        return note , liste_probleme

    
    def complexiter(self):
        comp_nb =1+ 10**self.nb_numero
        comp_cara_maj =1+ 26**self.nb_caratere_maj
        comp_cara_min =1+ 26**self.nb_caratere_min
        comp_cara_spe =1+ 42**self.nb_caratere_special
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
        return mdp
    
    
    
mot= Mot_de_passe(0, 0, 0, 0,3)
print(mot.complexiter())
print(mot.mdp)
# print(mot.upgrade_mot_de_passe())
