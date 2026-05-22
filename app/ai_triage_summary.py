# Import required libraries
import chromadb

from sentence_transformers import SentenceTransformer

from triage_rules import classify_failure
from triage_recommendations import recommend_actions


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB vector store
client = chromadb.PersistentClient(path="vectorstore")


# Load collection
collection = client.get_collection(
    name="regression_failures"
)


# Example incoming failure
incoming_failure = """
execution plan instability observed after optimizer statistics update
"""


# Convert incoming failure into embedding
query_embedding = model.encode(incoming_failure).tolist()


# Perform semantic similarity search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)


# Extract best match
best_document = results["documents"][0][0]
best_metadata = results["metadatas"][0][0]
best_distance = results["distances"][0][0]


# Build simplified failure object
failure = {
    "error": incoming_failure,
    "component": best_metadata.get("component"),
}


# Predict likely root-cause area
root_cause = classify_failure(failure)


# Generate recommendations
actions = recommend_actions(root_cause)


# Display AI triage summary
print("\nAI TRIAGE SUMMARY")
print("=" * 80)

print("\nIncoming Failure:")
print(incoming_failure)

print("\nMost Similar Historical Failure:")
print(best_document)

print(f"\nSemantic Distance : {best_distance:.4f}")

print(f"\nLikely Root Cause Area:")
print(root_cause)

print("\nRecommended Debugging Actions:")

for action in actions:
    print(f"- {action}")

print("\nSuggested Next Step:")
print(
    "Compare optimizer statistics refresh behavior and "
    "validate execution plan stability before and after change."
)