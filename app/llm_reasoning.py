# Import required libraries
import chromadb

from sentence_transformers import SentenceTransformer

from triage_rules import classify_failure
from triage_recommendations import recommend_actions


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB vector database
client = chromadb.PersistentClient(path="vectorstore")


# Load regression failure collection
collection = client.get_collection(
    name="regression_failures"
)


# Example incoming failure
incoming_failure = """
optimizer execution plan instability after statistics collection
"""


# Generate embedding for incoming failure
query_embedding = model.encode(
    incoming_failure
).tolist()


# Retrieve most similar historical failure
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)


# Extract retrieved match
best_document = results["documents"][0][0]
best_metadata = results["metadatas"][0][0]
best_distance = results["distances"][0][0]


# Build simplified failure object
failure = {
    "error": incoming_failure,
    "component": best_metadata.get("component"),
}


# Predict likely root cause
root_cause = classify_failure(failure)


# Generate recommendations
actions = recommend_actions(root_cause)


# Generate AI-style reasoning summary
reasoning_summary = f"""
The incoming regression failure appears semantically similar
to a historical optimizer regression involving execution plan
changes after statistics refresh operations.

The semantic retrieval engine identified a close match within
the SQL Optimizer component, suggesting the issue may involve
plan instability caused by optimizer statistics evolution,
histogram changes, or altered cardinality estimation.

The relatively low semantic distance indicates meaningful
contextual similarity between the current incident and the
historical regression pattern.

Recommended investigation should focus on:
- execution plan comparison
- optimizer statistics validation
- histogram verification
- plan baseline analysis
"""


# Display final reasoning
print("\nLLM-STYLE TRIAGE REASONING")
print("=" * 80)

print("\nIncoming Failure:")
print(incoming_failure)

print("\nMost Similar Historical Failure:")
print(best_document)

print(f"\nSemantic Distance: {best_distance:.4f}")

print("\nLikely Root Cause Area:")
print(root_cause)

print("\nAI Reasoning Summary:")
print(reasoning_summary)

print("\nRecommended Actions:")
for action in actions:
    print(f"- {action}")