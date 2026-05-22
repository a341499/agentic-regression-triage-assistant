# Import parser function from previous module
from parse_failures import parse_failures


# Function to classify likely root-cause area
def classify_failure(failure):

    # Extract important fields
    error = failure.get("error", "").lower()
    component = failure.get("component", "").lower()

    # Rule 1: Partition-related failures
    if "partition" in error or "partition" in component:
        return "Partition Metadata / Storage Layer"

    # Rule 2: Vector indexing failures
    elif "hnsw" in error or "vector" in component:
        return "Vector Index / Embedding Layer"

    # Rule 3: Optimizer plan instability
    elif "plan" in error or "optimizer" in component:
        return "SQL Optimizer / Statistics"

    # Rule 4: Data Guard / HA failures
    elif "redo" in error or "guard" in component:
        return "Replication / Recovery Layer"

    # Rule 5: Concurrency or locking issues
    elif "deadlock" in error:
        return "Concurrency / Transaction Layer"

    # Default fallback
    else:
        return "Unknown Root Cause"


# Main execution section
if __name__ == "__main__":

    # Parse regression failures
    failures = parse_failures("samples/sample_failures.txt")

    print("\nAI-Assisted Regression Triage")
    print("=" * 60)

    # Analyze each failure
    for idx, failure in enumerate(failures, start=1):

        root_cause = classify_failure(failure)

        print(f"\nFailure #{idx}")
        print(f"Test        : {failure.get('test')}")
        print(f"Error       : {failure.get('error')}")
        print(f"Severity    : {failure.get('severity')}")
        print(f"Likely Area : {root_cause}")