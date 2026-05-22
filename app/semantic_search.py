# Import required libraries
import chromadb

from sentence_transformers import SentenceTransformer


# Load semantic embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to persistent ChromaDB vector store
client = chromadb.PersistentClient(path="vectorstore")


# Load regression failure collection
collection = client.get_collection(
    name="regression_failures"
)


# Example incoming regression failure
query_text = """
execution plan instability observed after optimizer statistics update
"""


# Convert query into semantic embedding vector
query_embedding = model.encode(query_text).tolist()


# Perform semantic similarity search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)


# Display results
print("\nSemantic Search Results")
print("=" * 80)

print("\nIncoming Failure Query:")
print(query_text)

print("\nMost Similar Historical Failures:\n")


# Extract returned results
documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


# Print detailed matches
for idx, (document, metadata, distance) in enumerate(
    zip(documents, metadatas, distances),
    start=1
):

    print(f"Match #{idx}")
    print("-" * 80)

    # Similarity score
    print(f"Semantic Distance : {distance:.4f}")

    # Metadata fields
    print(f"Test Name         : {metadata.get('test')}")
    print(f"Component         : {metadata.get('component')}")
    print(f"Severity          : {metadata.get('severity')}")

    print("\nError:")
    print(metadata.get("error"))

    print("\nMatched Document:")
    print(document)

    print("=" * 80)