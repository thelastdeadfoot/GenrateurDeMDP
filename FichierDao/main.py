from MotDePasseDao import MotDePasseDao
from SiteDao import SiteDao

def main():
    #creer l'objet MotDePasseDao
    mdpDao=MotDePasseDao()

    #insert un seul mot de passe dans la base de données
    mdpDao.insertMdp(5, 2, 1, 1, "C5u!3", "Professionnel")

    data = [
    {"nbCaractere": "6", "nbNum": "3", "nbCarSpe": "2", "idSite": 1, "mdp": "abc123!", "categorie": "Professionnel"},
    {"nbCaractere": "8", "nbNum": "2", "nbCarSpe": "1", "idSite": 2, "mdp": "password$", "categorie": "Professionnel"},
    {"nbCaractere": "5", "nbNum": "1", "nbCarSpe": "0", "idSite": 3, "mdp": "qwerty", "categorie": "Personnel"},
    {"nbCaractere": "10", "nbNum": "4", "nbCarSpe": "3", "idSite": 4, "mdp": "secureP@ss", "categorie": "Personnel"}]

    #insert une liste dans la base de données
    mdpDao.insertMdpList(data)

    #recupere tout
    mdpDao.recupAllMdp()

    #recupere tout les mot de passe selon une colonne et une valeur 
    #ici, on cherche tout les mot de passe qui sont categoriser ""Professionnel
    mdpDao.recupMdpColonne("categorie", "Professionnel")

    #permet de recuperer un mot de passe choisie
    mdpDao.recupOneMdp("abc123!")

    #met a jour un mot de passe
    #abc123! devient simplement b
    mdpDao.updateMdp("abc123!", "b")

    #supprime un mot de passe
    mdpDao.supMdp(["C5u!3"])   
    
    dataAsup=["b", "password$", "qwerty", "secureP@ss"]
    #permet de supprimer un mot de passe via une liste
    mdpDao.supMdp(dataAsup)

    #creer l'objet SiteDao
    siteDao = SiteDao()
    
    #insert un site
    siteDao.insertSite("FaireDuPoridgeBonEtPasCher")

    data = [
    {"nomSite" : "Google"},
    {"nomSite" : "Facebook"},]
    #insert plusieurs site grace a une liste
    siteDao.insertSiteList(data)
       
    #met a jour un site
    siteDao.updateSite("FaireDuPoridgeBonEtPasCher", "FaireDuPoridge")

    #recuperer tout les site
    siteDao.recupAllSite()

    #recuper un seul site
    siteDao.recupOneSite("Facebook")

    #supprime un site
    siteDao.supSite(["FaireDuPoridge"])

    dataAsup=["Google", "Facebook"]
    #supprime un site via une liste
    siteDao.supSite(dataAsup)

if __name__ == "__main__":
    main()