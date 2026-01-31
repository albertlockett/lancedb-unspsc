import csv

import lancedb
from lancedb.pydantic import LanceModel, Vector
from pydantic import ConfigDict, Field
from sentence_transformers import SentenceTransformer


class UNSPSCProduct(LanceModel):
    """
    Modèle Pydantic pour représenter un produit UNSPSC avec son vecteur d'embedding.

    Hérite de LanceModel pour permettre l'intégration directe avec LanceDB.
    """

    model_config = ConfigDict(populate_by_name=True)

    key: str = Field(alias="Key")
    parent_key: str = Field(alias="Parent key")
    code: str = Field(alias="Code")
    title: str = Field(alias="Title")
    vector: Vector(384)  # Vecteur d'embedding de 384 dimensions


def load_table():
    """
    Charge les données UNSPSC depuis un fichier CSV, génère les embeddings
    et crée une table LanceDB pour la recherche vectorielle.
    """
    print("création de la table lancedb")

    # Charger le modèle d'embedding (s'exécute localement)
    print("chargement du modèle d'embedding...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Lire le fichier CSV
    with open("unspsc_codes.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Créer les embeddings pour tous les titres en batch
    print(f"création des embeddings pour {len(rows)} produits...")
    titles = [row["Title"] for row in rows]
    embeddings = model.encode(titles, show_progress_bar=True)

    # Créer les objets Pydantic avec les embeddings
    products = [
        UNSPSCProduct(
            key=row["Key"],
            parent_key=row["Parent key"],
            code=row["Code"],
            title=row["Title"],
            vector=embedding.tolist(),
        )
        for row, embedding in zip(rows, embeddings)
    ]

    print(f"terminé - dimension de l'embedding: {len(products[0].vector)}")

    # Afficher quelques exemples
    print("exemple de lignes:")
    for product in products[18:21]:
        print(f"{product.code}: {product.title}")
        print(f"  aperçu de l'embedding: {product.vector[:5]}...")

    # Connexion à la base de données LanceDB
    db = lancedb.connect("./db")

    # Supprimer la table si elle existe déjà
    if "unspc_codes" in db.list_tables().tables:
        print("suppression de la table avant création")
        db.drop_table("unspc_codes")

    # Créer la table et ajouter les données
    print("création de la table lance")
    table = db.create_table("unspc_codes", schema=UNSPSCProduct)
    table.add(products)


def query_table():
    """
    Effectue des recherches vectorielles sur la table LanceDB en utilisant
    des requêtes en langage naturel.
    """
    print("exécution des requêtes...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Ouvrir la connexion à la base de données
    db = lancedb.connect("./db")
    table = db.open_table("unspc_codes")

    # Liste de requêtes de test
    queries = [
        "Macbook Pro",
        "Cell Phone",
        "Scott Towel",
        "bouffe à chien",
        "automobile",
    ]

    # Afficher l'en-tête du tableau de résultats
    print("requête\t\tcode\t\ttitre")
    print("-------\t\t----\t\t-----")

    # Effectuer une recherche pour chaque requête
    for query in queries:
        # Générer l'embedding de la requête
        query_vec = model.encode_document(query)

        # Rechercher le produit le plus similaire
        results = table.search(query_vec.tolist()).limit(1).to_pydantic(UNSPSCProduct)
        result = results[0]

        print(f"{query}\t{result.code}\t{result.title}")


def main():
    """
    Fonction principale - POC de recherche vectorielle avec Pydantic et LanceDB.

    Démontre comment:
    1. Charger des données depuis un CSV
    2. Générer des embeddings avec sentence-transformers
    3. Créer une table LanceDB avec un schéma Pydantic
    4. Effectuer des recherches vectorielles
    """
    load_table()
    print("---")
    query_table()


if __name__ == "__main__":
    main()
