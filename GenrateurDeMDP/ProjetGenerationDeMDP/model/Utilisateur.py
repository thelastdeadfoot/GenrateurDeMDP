
class Utilisateur :
    def __init__(self,login, mdp):
        self.login = login
        self.mdp = mdp

    def get_login(self):
        return self.login

    def get_mdp(self):
        return self.mdp

    def set_mdp(self, mdp):
        self.mdp = mdp

    def set_login(self, login):
        self.login = login

    def hachage_mdp(self):
        print("oui il y en auras")