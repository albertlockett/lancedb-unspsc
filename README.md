# Recherche vectorielle UNSPSC avec LanceDB et Pydantic

[English follows](#english-version)

## Vue d'ensemble

Ce projet est une preuve de concept (POC) démontrant comment effectuer une recherche 
vectorielle sur des codes produits UNSPSC en utilisant Pydantic pour la validation des 
données et LanceDB comme base de données vectorielle.

Que sont les codes UNSPSC?

> Le Code normalisé des produits et services des Nations Unies® (UNSPSC®) est un système de classification mondial des produits et services.
> Ces codes sont utilisés pour classifier les produits et services : dans le cas des fournisseurs, pour classifier les produits et services de leur entreprise, et dans le cas des membres du personnel, pour classifier les produits et services lors de la publication d'opportunités d'approvisionnement.
> Pour plus d'informations, consultez cet article de notre Centre d'aide:

https://www.ungm.org/public/unspsc

## Fonctionnalités

- Chargement de codes UNSPSC depuis un fichier CSV
- Génération d'embeddings vectoriels avec `sentence-transformers`
- Validation des données avec Pydantic
- Stockage et recherche vectorielle avec LanceDB
- Recherche sémantique en langage naturel

## Prérequis

- Python 3.11+
- `uv` (gestionnaire de paquets Python)

## Installation
```bash
# Synchroniser les dépendances du projet
uv sync
```

## Utilisation
```bash
uv run example.py
```

Le script va:
1. Charger les codes UNSPSC depuis le CSV
2. Générer des embeddings pour chaque titre de produit
3. Créer une table LanceDB avec le schéma Pydantic
4. Effectuer des recherches vectorielles avec des requêtes exemples

## Exemple de requêtes

Le POC inclut des exemples de recherche:
- "Macbook Pro"
- "Cell Phone"
- "bouffe à chien"
- "automobile"

La recherche retourne le produit UNSPSC le plus similaire sémantiquement.

---

<a name="english-version"></a>

# UNSPSC Vector Search with LanceDB and Pydantic

## Overview

This project is a proof of concept (POC) demonstrating how to perform vector search on 
UNSPSC product codes using Pydantic for data validation and LanceDB as a vector database.

What are the UNSPSC codes?
> The United Nations Standard Products and Services Code® (UNSPSC®) is a global classification system of products and services.
> These codes are used to classify products and services: in the case of suppliers, to classify the products and services of their company, and in the case of Staff Members, to classify the products and services when publishing procurement opportunities. 
> For more information, read this article from our Help Center: 

https://www.ungm.org/public/unspsc

## Features

- Load UNSPSC codes from CSV file
- Generate vector embeddings with `sentence-transformers`
- Data validation with Pydantic
- Storage and vector search with LanceDB
- Semantic search in natural language

## Requirements

- Python 3.11+
- `uv` (Python package manager)

## Installation
```bash
# Install dependencies
uv sync
```

## Usage
```bash
uv run example.py
```

The script will:
1. Load UNSPSC codes from the CSV
2. Generate embeddings for each product title
3. Create a LanceDB table with the Pydantic schema
4. Perform vector searches with example queries

## License

MIT
