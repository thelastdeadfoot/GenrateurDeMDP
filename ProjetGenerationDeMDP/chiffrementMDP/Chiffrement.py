from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class Chiffrement:
    def __init__(self):
        # clé de cryptage (nombre de bit : 16, 24, 32, pour AES-128, AES-192, AES-256)
        self.key = b'balatroGOTY222222222222222222222'
        # ça j'ai pas compris, j'ai l'impression que c'est une deuxieme clé
        self.iv = b'MySuperSecretIV0'
        print("Instance de chiffrement créée")

    # Fonction pour crypter le mot de passe
    def crypteMDP(self, data):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode('utf-8'))
        padded_data += padder.finalize()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return ciphertext

    # Fonction pour décrypter un mot de passe
    def decrypteMDP(self, ciphertext):
        decryptor = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend()).decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_data)
        unpadded_data += unpadder.finalize()
        return unpadded_data.decode('utf-8')

#Exemple d'utilisation

#Creation de l'objet
chifr = Chiffrement()

#Le mot de passe
plaintext = "Ax#io5!4"

#Crypter le mot de passe
crypter = chifr.crypteMDP(plaintext)
print(f'Encrypted text: {crypter}')

#Decrypter le mot de passe
decrypter = chifr.decrypteMDP(crypter)
print(f'Decrypted text: {decrypter}')