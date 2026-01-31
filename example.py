import csv

import lancedb
from lancedb.pydantic import LanceModel, Vector
from pydantic import BaseModel, ConfigDict, Field
from sentence_transformers import SentenceTransformer


class UNSPSCProduct(LanceModel):
    model_config = ConfigDict(populate_by_name=True)

    key: str = Field(alias="Key")
    parent_key: str = Field(alias="Parent key")
    code: str = Field(alias="Code")
    title: str = Field(alias="Title")
    vector: Vector(384)


def load_table():
    print("creating lancedb table")

    print("loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Read CSV
    with open("unspsc_codes.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Create embeddings for all titles at once
    print(f"ceating embeddings for {len(rows)} products...")
    titles = [row["Title"] for row in rows]
    embeddings = model.encode(titles, show_progress_bar=True)

    # Create products WITH embeddings
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

    print(f"done - embedding dimension: {len(products[0].vector)}")

    # Example
    print("example row:")
    for product in products[18:21]:
        print(f"{product.code}: {product.title}")
        print(f"  embedding preview: {product.vector[:5]}...")

    db = lancedb.connect("./db")
    if "unspc_codes" in db.list_tables().tables:
        print("dropping table before create")
        db.drop_table("unspc_codes")

    print("creating lance table")
    table = db.create_table("unspc_codes", schema=UNSPSCProduct)
    table.add(products)


def query_table():
    print("executing queries ...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    db = lancedb.connect("./db")
    table = db.open_table("unspc_codes")

    queries = [
        "Macbook Pro",
        "Cell Phone",
        "Scott Towel",
        "bouff à chien",
        "automobile",
    ]

    print("query\t\tcode\t\ttitle")
    print("-----\t\t----\t\t-----")
    for query in queries:
        query_vec = model.encode_document(query)
        results = table.search(query_vec.tolist()).limit(1).to_pydantic(UNSPSCProduct)
        result = results[0]
        print(f"{query}\t{result.code}\t{result.title}")


def main():
    load_table()
    print("---")
    query_table()


if __name__ == "__main__":
    main()
