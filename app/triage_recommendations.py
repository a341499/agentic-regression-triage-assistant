# Import parser and classifier from existing project modules
from parse_failures import parse_failures
from triage_rules import classify_failure


# Function to suggest debugging recommendations
def recommend_actions(root_cause_area):
    # Recommendations based on likely root-cause area
    recommendations = {
        "Partition Metadata / Storage Layer": [
            "Check partition metadata consistency.",
            "Validate split/merge DDL execution path.",
            "Compare storage-level block mapping before and after operation.",
        ],
        "Vector Index / Embedding Layer": [
            "Validate vector index rebuild path.",
            "Check HNSW index consistency after DML or rebuild.",
            "Compare query results before and after vector index usage.",
        ],
        "SQL Optimizer / Statistics": [
            "Compare execution plans before and after stats refresh.",
            "Check optimizer statistics, histograms, and plan baselines.",
            "Validate whether plan change caused performance or correctness impact.",
        ],
        "Replication / Recovery Layer": [
            "Check redo apply lag and archive log availability.",
            "Validate standby synchronization state.",
            "Review failover/switchover timing and recovery logs.",
        ],
        "Concurrency / Transaction Layer": [
            "Review lock graph and wait events.",
            "Check concurrent DDL/DML interaction.",
            "Validate transaction ordering and deadlock trace.",
        ],
    }

    # Return recommendations, or fallback if area is unknown
    return recommendations.get(
        root_cause_area,
        ["Collect more logs and perform manual triage."]
    )


# Main execution section
if __name__ == "__main__":
    # Read and parse sample failures
    failures = parse_failures("samples/sample_failures.txt")

    print("\nAgentic Regression Triage Recommendations")
    print("=" * 70)

    # Classify each failure and print recommended actions
    for idx, failure in enumerate(failures, start=1):
        root_cause = classify_failure(failure)
        actions = recommend_actions(root_cause)

        print(f"\nFailure #{idx}")
        print(f"Test        : {failure.get('test')}")
        print(f"Error       : {failure.get('error')}")
        print(f"Severity    : {failure.get('severity')}")
        print(f"Likely Area : {root_cause}")

        print("Recommended Actions:")
        for action in actions:
            print(f"- {action}")