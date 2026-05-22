# Import required libraries
import requests
import chromadb
import streamlit as st

from sentence_transformers import SentenceTransformer

from triage_rules import classify_failure
from triage_recommendations import recommend_actions


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB vector store
client = chromadb.PersistentClient(path="vectorstore")


# Load regression failure collection
collection = client.get_collection(
    name="regression_failures"
)


# Streamlit page title
st.title("Agentic Regression Triage Assistant")


# Description
st.write(
    "AI-powered semantic regression triage using embeddings, "
    "vector search, Ollama LLM reasoning, recommendations, "
    "and upload-based log analysis."
)


# Text input option
incoming_failure = st.text_area(
    "Enter regression failure description:",
    height=150
)


# File upload option
uploaded_file = st.file_uploader(
    "Or upload a regression log / incident text file:",
    type=["txt", "log"]
)


# Extract uploaded file content if present
uploaded_text = ""

if uploaded_file is not None:
    uploaded_text = uploaded_file.read().decode("utf-8", errors="ignore")
    st.write("### Uploaded File Preview")
    st.code(uploaded_text[:2000])


# Choose final input source
final_failure_text = uploaded_text if uploaded_text.strip() else incoming_failure


# Run analysis button
if st.button("Run AI Triage"):

    if final_failure_text.strip():

        query_embedding = model.encode(
            final_failure_text
        ).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        best_document = documents[0]
        best_metadata = metadatas[0]
        best_distance = distances[0]

        failure = {
            "error": final_failure_text,
            "component": best_metadata.get("component"),
        }

        root_cause = classify_failure(failure)
        actions = recommend_actions(root_cause)

        prompt = f"""
You are an AI regression triage assistant.

Incoming Failure:
{final_failure_text}

Most Similar Historical Failure:
{best_document}

Semantic Distance:
{best_distance:.4f}

Likely Root Cause Area:
{root_cause}

Recommended Actions:
{actions}

Generate a concise technical triage reasoning summary.
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False,
            },
        )

        llm_output = response.json().get(
            "response",
            "LLM reasoning unavailable. Please check Ollama server/model."
        )

        st.subheader("AI Triage Summary")

        st.write("### Incoming Failure")
        st.write(final_failure_text)

        st.write("### Likely Root Cause Area")
        st.write(root_cause)

        st.write("### LLM-Generated Reasoning")
        st.write(llm_output)

        st.write("### Recommended Debugging Actions")
        for action in actions:
            st.write(f"- {action}")

        st.write("### Top Similar Historical Failures")

        for idx, (document, metadata, distance) in enumerate(
            zip(documents, metadatas, distances),
            start=1
        ):
            st.write(f"#### Match #{idx}")
            st.write(f"**Semantic Distance:** {distance:.4f}")
            st.write(f"**Test:** {metadata.get('test')}")
            st.write(f"**Component:** {metadata.get('component')}")
            st.write(f"**Severity:** {metadata.get('severity')}")
            st.code(document)

    else:
        st.warning("Please enter text or upload a log file.")