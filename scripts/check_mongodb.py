from pymongo import MongoClient

def check_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # Essayer de lister les bases de données pour vérifier la connexion
        print("Connexion à MongoDB réussie :", client.list_database_names())
    except Exception as e:
        print("Erreur de connexion :", e)

if __name__ == "__main__":
    check_connection()