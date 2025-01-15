import random
class Mot_de_passe :

    def comparer(self):
        try:
            with open('mdp20000.txt', 'r') as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if ligne == self.mdp:
                        return "Mot de passe trop commun"
                
                return "Mot de passe unique"
                        
        except FileNotFoundError:
            return "Erreur: Le fichier mdp1000.txt n'a pas été trouvé"
        except Exception as e:
            return f"Erreur lors de la lecture du fichier: {str(e)}"


    def __init__(self,nb_caratere_maj,nb_caratere_min,nb_numero,nb_caratere_special,mot_de_passe=None):
        
        
        if mot_de_passe == None:
            self.taille = nb_caratere_maj + nb_caratere_min + nb_numero + nb_caratere_special
            self.mdp = self.genere_mot_de_passe(nb_caratere_maj,nb_caratere_min,nb_numero,nb_caratere_special)
            self.nb_caratere_maj = nb_caratere_maj
            self.nb_caratere_min = nb_caratere_min
            self.nb_numero = nb_numero
            self.nb_caratere_special = nb_caratere_special
        else :
            self.mdp = mot_de_passe
            self.taille = len(mot_de_passe)
            self.nb_caratere_maj = 0
            self.nb_caratere_min = 0
            self.nb_numero = 0
            self.nb_caratere_special = 0
            for lettre in mot_de_passe:
                
                if 33 <= ord(lettre) <= 47 :
                    self.nb_caratere_special += 1
                    
                if 48 <= ord(lettre) <= 57 :
                    self.nb_numero += 1
                    
                if 65 <= ord(lettre) <= 90 :
                    self.nb_caratere_maj += 1
                    
                if 97 <= ord(lettre) <= 122 :
                    self.nb_caratere_maj += 1
                    
                    
                    
    def upgrade_robustesse (self):
        if self.verifier_robustesse_mdp() == "trop court":
            print("votre mdp est maintenet Moyennement robuste passer le une fois de plus dans la methode pour plus de robustest")
            for i in range (8-self.taille):
                variable = random.randint(33, 47)

                variable = chr(variable)
                self.mdp += variable
        elif self.verifier_robustesse_mdp() == "Pas robuste":
            print("votre mdp est maintenet Moyennement robuste passer le une fois de plus dans la methode pour plus de robustest")
            
            variable = random.randint(33, 47)
            variable = chr(variable)
            self.mdp += variable
            
            variable = random.randint(48, 57)
            variable = chr(variable)
            self.mdp += variable
            
            variable = random.randint(65, 90)
            variable = chr(variable)
            self.mdp += variable
        
        elif self.verifier_robustesse_mdp() == "Moyennement robuste":
            print("votre mdp est maintenet Robuste")
            for i in range (12-self.taille):
                variable = random.randint(33, 47)

                variable = chr(variable)
                self.mdp += variable
    
    def verifier_robustesse_mdp(self):
    # Vérifier la longueur du mot de passe
        if len(self.get_mdp()) < 8:
            return "trop court"
        
        # Vérifier les critères de "pleinement robuste"
        elif len(self.get_mdp()) >= 12 and self.nb_caratere_min != 0 and self.nb_caratere_maj != 0 and self.nb_numero != 0 and self.nb_caratere_special != 0 :
            return "Pleinement robuste"
        
        # Vérifier les critères de "moyennement robuste"
        elif (8 <= len(self.get_mdp()) < 12) and self.nb_caratere_maj != 0 or self.nb_numero != 0 and self.nb_caratere_min != 0:
            return "Moyennement robuste"
        
        # Si aucune des conditions ci-dessus n'est remplie
        return "Pas robuste"

    


    def get_mdp(self):
        return self.mdp
    
    def get_taille(self):
        return self.taille
    
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
            variable = random.randint(33, 47)

            variable = chr(variable)
            mdp += variable
        mdp = ''.join(random.sample(mdp,len(mdp)))
        return mdp
