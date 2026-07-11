from pymongo import MongoClient

def check_connection():
    """
    Script de test de connectivité réseau pour Windows (Localhost).
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        databases = client.list_database_names()
        print("Connexion établie avec succès !")
        print("Bases de données trouvées :", databases)
        
        client.close()
    except Exception as e:
        print("Erreur de connexion :")
        print(e)

if __name__ == "__main__":
    check_connection()