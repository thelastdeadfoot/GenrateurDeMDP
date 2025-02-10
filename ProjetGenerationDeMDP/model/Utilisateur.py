
class Utilisateur :
    def __init__(self,login, mdp):
        self.login = login
        self.mdp = mdp

    def getLogin(self):
        return self.login

    def getMdp(self):
        return self.mdp

    def setMdp(self, mdp):
        self.mdp = mdp

    def setLogin(self, login):
        self.login = login

    def hachageMdp(self):
        print("oui il y en auras")