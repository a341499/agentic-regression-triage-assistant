# Import required libraries
import json
from pathlib import Path

from parse_failures import parse_failures
from triage_rules import classify_failure
from triage_recommendations import recommend_actions


# Function to generate structured JSON output
def generate_json(output_file):

    # Parse regression failures
    failures = parse_failures("samples/sample_failures.txt")

    # Final structured output list
    triage_results = []

    # Process each failure
    for failure in failures:

        # Identify likely root-cause area
        root_cause = classify_failure(failure)

        # Generate debugging recommendations
        actions = recommend_actions(root_cause)

        # Create structured triage object
        triage_entry = {
            "test": failure.get("test"),
            "error": failure.get("error"),
            "component": failure.get("component"),
            "severity": failure.get("severity"),
            "likely_root_cause": root_cause,
            "recommended_actions": actions,
        }

        # Add to final results
        triage_results.append(triage_entry)

    # Write JSON output to file
    Path(output_file).write_text(
        json.dumps(triage_results, indent=4),
        encoding="utf-8"
    )

    print("\nJSON triage output generated successfully:")
    print(output_file)


# Main execution section
if __name__ == "__main__":

    # Output JSON file path
    output_path = "logs/triage_output.json"

    # Generate JSON output
    generate_json(output_path)