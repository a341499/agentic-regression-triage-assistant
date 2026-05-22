# Import required project modules
from pathlib import Path

from parse_failures import parse_failures
from triage_rules import classify_failure
from triage_recommendations import recommend_actions


# Function to generate triage report
def generate_report(output_file):

    # Parse all regression failures
    failures = parse_failures("samples/sample_failures.txt")

    # List to collect report lines
    report_lines = []

    # Report title
    report_lines.append("AGENTIC REGRESSION TRIAGE REPORT")
    report_lines.append("=" * 80)

    # Process each failure
    for idx, failure in enumerate(failures, start=1):

        # Classify likely root-cause area
        root_cause = classify_failure(failure)

        # Generate recommendations
        actions = recommend_actions(root_cause)

        # Add formatted report content
        report_lines.append(f"\nFailure #{idx}")
        report_lines.append(f"Test        : {failure.get('test')}")
        report_lines.append(f"Error       : {failure.get('error')}")
        report_lines.append(f"Component   : {failure.get('component')}")
        report_lines.append(f"Severity    : {failure.get('severity')}")
        report_lines.append(f"Likely Area : {root_cause}")

        report_lines.append("Recommended Actions:")

        for action in actions:
            report_lines.append(f"- {action}")

        report_lines.append("-" * 80)

    # Write report to output file
    Path(output_file).write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )

    print(f"\nTriage report generated successfully:")
    print(output_file)


# Main execution section
if __name__ == "__main__":

    # Output report location
    output_path = "logs/triage_report.txt"

    # Generate report
    generate_report(output_path)