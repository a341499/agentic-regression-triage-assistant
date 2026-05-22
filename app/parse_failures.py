# Import Path utility for easier file handling
from pathlib import Path


# Function to read and parse regression failures
def parse_failures(file_path):

    # Read the entire file content as text
    content = Path(file_path).read_text(encoding="utf-8")

    # Each failure block is separated by a blank line
    blocks = content.strip().split("\n\n")

    # List to store parsed failures
    failures = []

    # Process each failure block
    for block in blocks:

        # Dictionary to store one parsed failure
        failure = {}

        # Process each line inside the block
        for line in block.splitlines():

            # Only process lines containing key:value pairs
            if ":" in line:

                # Split only at first colon
                key, value = line.split(":", 1)

                # Store normalized key and cleaned value
                failure[key.strip().lower()] = value.strip()

        # Add parsed failure to final list
        failures.append(failure)

    # Return all parsed failures
    return failures


# Main execution entry point
if __name__ == "__main__":

    # Parse the sample regression failure file
    failures = parse_failures("samples/sample_failures.txt")

    # Display parsed results
    print("\nParsed Regression Failures:")
    print("-" * 60)

    # Print each parsed failure cleanly
    for idx, failure in enumerate(failures, start=1):

        print(f"\nFailure #{idx}")
        print(f"Test      : {failure.get('test')}")
        print(f"Error     : {failure.get('error')}")
        print(f"Component : {failure.get('component')}")
        print(f"Severity  : {failure.get('severity')}")