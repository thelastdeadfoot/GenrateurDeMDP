from MotDePasseDao import MotDePasseDao
from SiteDao import SiteDao
from UtilisateurDao import UtilisateurDao

# ___________________PARTIE MOT DE PASSE__________________________________________________
# creer l'objet MotDePasseDao
mdpDao = MotDePasseDao()

# insert un seul mot de passe dans la base de données
mdpDao.insert_mdp(5, 2, 1, 1, "C5u!3", "Professionnel", 126, 1, 2, 2)

data = [
    {"nbCaractere": "6", "nbNum": "3", "nbCarSpe": "2", "idSite": 1, "mdp": "abc123!", "categorie": "Professionnel",
     "idUtilisateur": 126, "Robustesse": 4, "carMini": 2, "carMaj": 2},
    {"nbCaractere": "8", "nbNum": "2", "nbCarSpe": "1", "idSite": 2, "mdp": "password$", "categorie": "Professionnel",
     "idUtilisateur": 126, "Robustesse": 8, "carMini": 2, "carMaj": 2},
    {"nbCaractere": "5", "nbNum": "1", "nbCarSpe": "0", "idSite": 3, "mdp": "qwerty", "categorie": "Personnel",
     "idUtilisateur": 126, "Robustesse": 1, "carMini": 2, "carMaj": 2},
    {"nbCaractere": "10", "nbNum": "4", "nbCarSpe": "3", "idSite": 4, "mdp": "secureP@ss", "categorie": "Personnel",
     "idUtilisateur": 126, "Robustesse": 14, "carMini": 2, "carMaj": 2}]

# insert une liste dans la base de données
mdpDao.insert_mdp_list(data)

# recupere tout
mdpDao.recup_all_mdp()

# recupere tout les mot de passe selon une colonne et une valeur
# ici, on cherche tout les mot de passe qui sont categoriser "Professionnel"
mdpDao.recup_mdp_colonne("categorie", "Professionnel")

# permet de recuperer un mot de passe choisie
mdpDao.recup_one_mdp("abc123!")

# met a jour un mot de passe
# abc123! devient simplement b
mdpDao.update_mdp("abc123!", "b")

# met a jour la colonne du nombre de caractère du mot de passe "b"
mdpDao.update_nb_caractere("b", 3)

# met a jour la colonne du nombre de caractère,spéciaux du mot de passe "b"
mdpDao.update_nb_car_spe("b", 4)

# met a jour la colonne du nombre de nombre du mot de passe "b"
mdpDao.update_nb_num("b", 5)

# met a jour la colonne de la categorie du mot de passe "b"
mdpDao.update_mdp_categorie("b", "Personnel")

# met a jour la colonne de la robustesse du mot de passe "b"
mdpDao.update_mdp_robustesse("b", 2)

# met a jour la colonne de carMini du mot de passe "b"
mdpDao.update_mdp_car_mini("b", 4)

# met a jour la colonne de carMaj du mot de passe "b"
mdpDao.update_mdp_car_maj("b", 4)

# supprime un mot de passe
mdpDao.sup_mdp(["C5u!3"])

dataAsup = ["b", "password$", "qwerty", "secureP@ss"]
# permet de supprimer un mot de passe via une liste
mdpDao.sup_mdp(dataAsup)

# _______________________PARTIE SITE___________________________
# creer l'objet SiteDao
site_dao = SiteDao()

# insert un site
site_dao.insert_site("FaireDuPoridgeBonEtPasCher")

data = [
    {"nomSite": "Google"},
    {"nomSite": "Facebook"}, ]
# insert plusieurs site grace a une liste
site_dao.insert_site_list(data)

# met a jour un site
site_dao.update_site("FaireDuPoridgeBonEtPasCher", "FaireDuPoridge")

# recuperer tout les site
site_dao.recup_all_site()

# recuper un seul site
site_dao.recup_one_site("Facebook")

# supprime un site
site_dao.sup_site(["FaireDuPoridge"])

dataAsup = ["Google", "Facebook"]
# supprime un site via une liste
site_dao.sup_site(dataAsup)

# ____________________________PARTIE UTILISATEUR________________________________
# Crée l'objet qui te permettras d'intereagire avec la base de données
user_dao = UtilisateurDao()

# Exemple d'utilisation pour inserer un utilisateur
user_dao.insert_user("dude", "LeMotDePasseDeDude")

data = [
    {"login": "guys", "mdpMaitre": "guysPassword"},
    {"login": "mec", "mdpMaitre": "leMdpDuMec"}, ]
# Exemple pour inserer plusieurs utilisateur via une liste (inutile vu notre app, mais au cas ou)
user_dao.insert_user_list(data)

# Recuperer la la liste de tout les utilisateurs
user_dao.recup_all_user()

# Recuperer un seul utilisateur
user_dao.recup_one_user("dude")

# Mettre un jour un mot de passe maitre d'un utilisateur
user_dao.update_mdp("guysPassword", "gp", "guys")

# Permet de mettre a jour un login d'un utilisateur
user_dao.update_user("guys", "guy")

# Permet de chercher un mot de passe selon un utilisateur
user_dao.cherche_mdp_selon_user("mec")

# Permet de supprimer plusieurs ou 1 utilisateurs selon une liste
# Si les utilisateurs ont des mot de passe associée dans le coffre a mdp, ne pas oublier de faire ça :
# mdpDao.supMdpSelonUsers(["mec", "guy", "dude"])
user_dao.sup_user(["mec", "guy", "dude"])

# Verifie si Jean-Huges existe dans la base de données
user_dao.verif_user("Jean-Huges", "oui")