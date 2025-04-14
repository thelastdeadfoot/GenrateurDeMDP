import os
import psycopg2
from supabase import create_client, Client

# Définition des clés d'environnement
os.environ["SUPABASE_URL"] = "https://vijrfostiknzlxhbsgwy.supabase.co"
os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpanJmb3N0aWtuemx4aGJzZ3d5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY4NDc5NjgsImV4cCI6MjA1MjQyMzk2OH0.w3FWw1e6859mozW_I89UfxglgaEdnrIQFfnDzbCuj8g"

# Récupérer l'URL et la clé à partir des variables d'environnement
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Créer le client Supabase
supabase: Client = create_client(url, key)

class MotDePasseDao:
    def __init__(self):
        print("Instance de MotDePasseDao créée.")

    # Insertion d'un seul mot de passe
    def insert_mdp(self, nbCaractere, nbNum, nbCarSpe, idSite, mdp, categorie, idUtilisateur, Robuste, carMini, carMaj):
        print("Insertion de donnée mdp : " +mdp)
        data = {"nbCaractere": nbCaractere, "nbNum": nbNum, "nbCarSpe": nbCarSpe, "idSite": idSite, "mdp": mdp, "categorie": categorie, "idUtilisateur" : idUtilisateur, "Robustesse": Robuste, "carMini" : carMini, "carMaj" : carMaj}
        response = supabase.table("MotDePasse").insert(data).execute()
        print(f"Voici le mot de passe et ses caractéristique qui vont être envoyée : {response.data}")
        return response.data
        
    # Insertion de mot de passe via une liste
    def insert_mdp_list(self, data):
        print("Insertion des données mdp")
        response = supabase.table("MotDePasse").insert(data).execute()
        #ci-dessous, permet d'inserer des elements en excluant les doublons se trouvant dans la liste
        # response = supabase.table("MotDePasse").upsert(data).execute()
        print(response.data)
        return response.data

    # Récupérer toutes les mots de passe
    def recup_all_mdp(self):
        print("Récupération des données mdp")
        response = supabase.table("MotDePasse").select("*").execute()
        print(response.data)
        return response.data

    # Récupérer les mots de passe selon une colonne et une valeur 
    # (par exemple, pour recuperer tout les catégorie qui sont égale a "Professionnel")
    def recup_mdp_colonne(self, colonne, valeur):
        print("Récupération des données mdp de valeur : "+valeur+"\n colonne : "+colonne)
        response = supabase.table("MotDePasse").select("*").eq(colonne, valeur).execute()
        print(response.data)
        return response.data

    # Récupérer un mot de passe
    def recup_one_mdp(self, mdp_a_chercher):
        print("Récupération de la donnée "+ mdp_a_chercher)
        response = supabase.table("MotDePasse").select("mdp").eq("mdp", mdp_a_chercher).execute()
        print(response.data)
        return response.data

    # Met a jour un mot de passe
    def update_mdp(self,new_mdp,nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("mise a jour du mdp")
        try:
            # Informations de connexion
            conn = psycopg2.connect("postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            if categorie is not None:
                query = """
                        UPDATE "MotDePasse"
                        SET "mdp" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" = %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            else:
                query = """
                        UPDATE "MotDePasse"
                        SET "mdp" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" IS %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            _vars = (new_mdp, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()
            print("mise a jour réussie du mdp")
        except Exception as e:
            print(f"Erreur lors de la mise a jour : {e}")

    # Met a jour le site d'un mot de passe
    def update_site(self, new_site, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("mise a jour du mdp")
        try:
            # Informations de connexion
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            if categorie is not None:
                query = """
                                UPDATE "MotDePasse"
                                SET "idSite" = %s
                                WHERE "nbCaractere" = %s
                                AND "nbNum" = %s
                                AND "nbCarSpe" = %s
                                AND "idSite" = %s
                                AND "mdp" = %s
                                AND "categorie" = %s
                                AND "idUtilisateur" = %s
                                AND "carMini" = %s
                                AND "carMaj" = %s
                                """
            else:
                query = """
                                UPDATE "MotDePasse"
                                SET "idSite" = %s
                                WHERE "nbCaractere" = %s
                                AND "nbNum" = %s
                                AND "nbCarSpe" = %s
                                AND "idSite" = %s
                                AND "mdp" = %s
                                AND "categorie" IS %s
                                AND "idUtilisateur" = %s
                                AND "carMini" = %s
                                AND "carMaj" = %s
                                """
            _vars = (new_site, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()
            print("mise a jour réussie du site")
        except Exception as e:
            print(f"Erreur lors de la mise a jour : {e}")
    
    # Met a jour la colonne du nombre de caractère d'un mot de passe donner
    def update_nb_caractere(self,new_nb_caractere,nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("mise a jour du nombre de caractère")
        try:
            # Informations de connexion
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            if categorie is not None:
                query = """
                    UPDATE "MotDePasse"
                       SET "nbCaractere" = %s
                     WHERE "nbCaractere" = %s
                       AND "nbNum" = %s
                       AND "nbCarSpe" = %s
                       AND "idSite" = %s
                       AND "mdp" = %s
                       AND "categorie" = %s
                       AND "idUtilisateur" = %s
                       AND "carMini" = %s
                       AND "carMaj" = %s
                    """
            else:
                query = """
                        UPDATE "MotDePasse"
                           SET "nbCaractere" = %s
                         WHERE "nbCaractere" = %s
                           AND "nbNum" = %s
                           AND "nbCarSpe" = %s
                           AND "idSite" = %s
                           AND "mdp" = %s
                           AND "categorie" IS %s
                           AND "idUtilisateur" = %s
                           AND "carMini" = %s
                           AND "carMaj" = %s
                        """
            _vars = (new_nb_caractere, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()
            print("mise a jour réussie du nombre de caractères")
        except Exception as e:
            print(f"Erreur lors de la mise a jour : {e}")

#self,new_nb_caractere,nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj
    # Met a jour la colonne du nombre de de numéro d'un mot de passe donner
    def update_nb_num(self,new_nb_num,nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("mise a jour du nombre de chiffre")
        try:
            # Informations de connexion
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            if categorie is not None:
                query = """
                        UPDATE "MotDePasse"
                        SET "nbNum" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" = %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            else:
                query = """
                        UPDATE "MotDePasse"
                        SET "nbNum" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" IS %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            _vars = (new_nb_num, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()
            print("mise a jour réussie du nombre de chiffre")
        except Exception as e:
            print(f"Erreur lors de la mise a jour : {e}")
    
    # Met a jour la colonne du nombre de caractère spéciaux d'un mot de passe donner
    def update_nb_car_spe(self, new_nb_car_spe,nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("mise a jour du nombre de caractères speciaux")
        try:
            # Informations de connexion
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            if categorie is not None:
                query = """
                        UPDATE "MotDePasse"
                        SET "nbCarSpe" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" = %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            else:
                query = """
                        UPDATE "MotDePasse"
                        SET "nbCarSpe" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" IS %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            _vars = (new_nb_car_spe, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()
            print("mise a jour réussie du nombre de caractères speciaux")
        except Exception as e:
            print(f"Erreur lors de la mise a jour : {e}")
    
    # Met a jour la colonne categorie d'un mot de passe donner
    def update_mdp_categorie(self,new_categorie,nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("mise a jour du nombre de caractère")
        try:
            # Informations de connexion
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            if categorie is not None:
                query = """
                        UPDATE "MotDePasse"
                        SET "categorie" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" = %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            else:
                query = """
                        UPDATE "MotDePasse"
                        SET "categorie" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" IS %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            _vars = (new_categorie, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()
            print("mise a jour réussie du nombre de chiffre")
        except Exception as e:
            print(f"Erreur lors de la mise a jour : {e}")

    # Met a jour la colonne robuste d'un mot de passe donner
    # A mettre a jour du coup, je le ferais quand robustesse seras bien putaing
    def update_mdp_robustesse(self, mdp, nv_rob_mdp):
        print("Mise à jour de la donnée mdp : "+ mdp)
        response = supabase.table("MotDePasse").update({"Robustesse": nv_rob_mdp}).eq("mdp", mdp).execute()
        print(response.data)
        return response.data
    
    # Met a jour la colonne carMini d'un mot de passe donner
    def update_mdp_car_mini(self,new_car_mini,nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("mise a jour du nombre de mini caractère")
        try:
            # Informations de connexion
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            if categorie is not None:
                query = """
                        UPDATE "MotDePasse"
                        SET "carMini" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" = %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            else:
                query = """
                        UPDATE "MotDePasse"
                        SET "carMini" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" IS %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            _vars = (new_car_mini, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()
            print("mise a jour réussie du nombre de mini caractère")
        except Exception as e:
            print(f"Erreur lors de la mise a jour : {e}")
    
    # Met a jour la colonne carMaj d'un mot de passe donner
    def update_mdp_car_maj(self, new_car_maj, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("mise a jour du nombre de gros caractère")
        try:
            # Informations de connexion
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            if categorie is not None:
                query = """
                        UPDATE "MotDePasse"
                        SET "carMaj" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" = %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            else:
                query = """
                        UPDATE "MotDePasse"
                        SET "carMaj" = %s
                        WHERE "nbCaractere" = %s
                        AND "nbNum" = %s
                        AND "nbCarSpe" = %s
                        AND "idSite" = %s
                        AND "mdp" = %s
                        AND "categorie" IS %s
                        AND "idUtilisateur" = %s
                        AND "carMini" = %s
                        AND "carMaj" = %s
                        """
            _vars = (new_car_maj, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()
            print("mise a jour réussie du nombre de gros caractère")
        except Exception as e:
            print(f"Erreur lors de la mise a jour : {e}")
    
    # permet de supprimer tout les mots de passe d'un user
    # oui, je suis obliger d'utiliser une autre api pour pouvoir executer des requete en brute
    # (oui, c'est plus chiant pour comprendre)
    # en plus on est obliger de fermer la connexion manuellement
    def sup_mdp_selon_users(self, users_a_sup):
        print(f"Suppression des mots de passe pour les utilisateurs : ")
        try:
            # Informations de connexion
            conn = psycopg2.connect("postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()
            
            # requete en dur car l'api supabase ne supporte pas les jointure dans le delete
            query = """
            DELETE FROM "MotDePasse"
            USING "Utilisateurs"
            WHERE "MotDePasse"."idUtilisateur" = "Utilisateurs"."idUtilisateur"
            AND "Utilisateurs"."login" IN %s;
            """
            
            cur.execute(query, (tuple(users_a_sup),))
            conn.commit()
            
            print("Suppression réussie pour les utilisateurs : ")
        
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
        
        finally:
            if conn:
                conn.close()
                print("Connexion à la base de données fermée.")

    def sup_un_mdp_selon_users(self, nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj):
        print("Suppression du mot de passe pour l'utilisateur : ", id_utilisateur)
        try:
            # Informations de connexion
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres")
            cur = conn.cursor()

            # requete en dur car l'api supabase ne supporte pas les jointure dans le delete
            if categorie is not None:
                query = """
                DELETE FROM "MotDePasse"
                WHERE "nbCaractere" = %s
                  AND "nbNum" = %s
                  AND "nbCarSpe" = %s
                  AND "idSite" = %s
                  AND "mdp" = %s
                  AND "categorie" = %s
                  AND "idUtilisateur" = %s
                  AND "carMini" = %s
                  AND "carMaj" = %s
                """
            else:
                query = """
                    DELETE FROM "MotDePasse"
                    WHERE "nbCaractere" = %s
                    AND "nbNum" = %s
                    AND "nbCarSpe" = %s
                    AND "idSite" = %s
                    AND "mdp" = %s
                    AND "categorie" IS %s
                    AND "idUtilisateur" = %s
                    AND "carMini" = %s
                    AND "carMaj" = %s
                    """
            _vars = (nb_caractere, nb_num, nb_car_spe, id_site, mdp, categorie, id_utilisateur, car_mini, car_maj)
            print(cur.mogrify(query, _vars).decode('utf-8'))
            cur.execute(query, _vars)
            conn.commit()

        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")

    def recup_all_mdp_user(self, login, mdp):
        print(f"Récupération des mots de passe pour l'utilisateur : {login}")

        try:
            # Connexion à la base de données
            conn = psycopg2.connect(
                "postgresql://postgres:bZ60rQPU8FHKHjwi@db.vijrfostiknzlxhbsgwy.supabase.co:5432/postgres"
            )
            cur = conn.cursor()
            query = """
            SELECT "mdp", "idSite", "categorie", "nbCaractere", "nbNum", "nbCarSpe", "carMini", "carMaj"  
            FROM "MotDePasse"
            INNER JOIN "Utilisateurs" ON "MotDePasse"."idUtilisateur" = "Utilisateurs"."idUtilisateur"
            WHERE "Utilisateurs"."login" = %s AND "Utilisateurs"."mdpMaitre" = %s
            """
            cur.execute(query, (login, mdp))

            rows = cur.fetchall()

            cur.close()
            conn.close()

            print(f"Nombre de résultats trouvés : {len(rows)}")
            return rows

        except Exception as e:
            print(f"Erreur lors de la récupération : {e}")
            return []