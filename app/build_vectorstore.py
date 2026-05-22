# Import required libraries
import chromadb

from sentence_transformers import SentenceTransformer

from parse_failures import parse_failures


# Load embedding model
# This model converts text into semantic vectors
model = SentenceTransformer("all-MiniLM-L6-v2")


# Initialize ChromaDB persistent client
client = chromadb.PersistentClient(path="vectorstore")


# Create or load collection
collection = client.get_or_create_collection(
    name="regression_failures"
)


# Read regression failure dataset
failures = parse_failures("samples/sample_failures.txt")


# Process each failure
for idx, failure in enumerate(failures):

    # Build searchable text document
    document = f"""
    Test: {failure.get('test')}
    Error: {failure.get('error')}
    Component: {failure.get('component')}
    Severity: {failure.get('severity')}
    """

    # Generate semantic embedding vector
    embedding = model.encode(document).tolist()

    # Store into ChromaDB
    collection.add(
        ids=[str(idx)],
        documents=[document],
        embeddings=[embedding],
        metadatas=[failure]
    )

    print(f"Indexed failure #{idx + 1}")


print("\nVector store build completed successfully.")