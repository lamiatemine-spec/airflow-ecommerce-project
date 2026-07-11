from pymongo import MongoClient

def check_connection():
    """
    Script de test de connectivité réseau entre Airflow et MongoDB.
    Utilise le nom de service 'ecommerce_mongodb' tel que défini dans docker-compose.
    """
    try:
        # Connexion au service MongoDB via le réseau interne Docker
        client = MongoClient("mongodb://ecommerce_mongodb:27017/", serverSelectionTimeoutMS=5000) 
        
        # Test effectif de la connexion en listant les bases de données
        databases = client.list_database_names()
        print("Connexion établie avec succès !")
        print("Bases de données trouvées :", databases)
        
        client.close()
    except Exception as e:
        print("Erreur de connexion :")
        print(e)

if __name__ == "__main__":
    check_connection()