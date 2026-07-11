from pymongo import MongoClient

def test_connection():
    uri = "mongodb://ecommerce_mongodb:27017/"
    print(f"Tentative de connexion à : {uri}")
    try:
        client = MongoClient("mongodb://admin:password@ecommerce_mongodb:27017/?authSource=admin", serverSelectionTimeoutMS=5000)
        db_list = client.list_database_names()
        print("✅ Connexion réussie !")
        print("Bases de données disponibles :", db_list)
        client.close()
    except Exception as e:
        print("❌ Erreur de connexion :")
        print(e)

if __name__ == "__main__":
    test_connection()
