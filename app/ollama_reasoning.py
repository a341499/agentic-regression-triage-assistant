# Import required libraries
import requests
import chromadb

from sentence_transformers import SentenceTransformer

from triage_rules import classify_failure
from triage_recommendations import recommend_actions


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB vector database
client = chromadb.PersistentClient(path="vectorstore")


# Load collection
collection = client.get_collection(
    name="regression_failures"
)


# Example incoming failure
incoming_failure = """
optimizer execution plan instability after statistics collection
"""


# Generate embedding
query_embedding = model.encode(
    incoming_failure
).tolist()


# Perform semantic retrieval
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)


# Extract best historical match
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


# Build LLM prompt
prompt = f"""
You are an AI regression triage assistant.

Incoming Failure:
{incoming_failure}

Most Similar Historical Failure:
{best_document}

Likely Root Cause Area:
{root_cause}

Recommended Actions:
{actions}

Generate a concise technical triage reasoning summary.
"""


# Send prompt to Ollama local LLM
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }
)


# Extract generated response
llm_output = response.json()["response"]


# Display final output
print("\nOLLAMA AI TRIAGE REASONING")
print("=" * 80)

print("\nIncoming Failure:")
print(incoming_failure)

print("\nMost Similar Historical Failure:")
print(best_document)

print(f"\nSemantic Distance: {best_distance:.4f}")

print("\nLikely Root Cause Area:")
print(root_cause)

print("\nLLM-Generated Reasoning:")
print(llm_output)

print("\nRecommended Actions:")
for action in actions:
    print(f"- {action}")