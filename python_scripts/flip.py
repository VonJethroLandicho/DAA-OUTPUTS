"""
Project Title: Boolean Value Flipper for CSV Files

Description:
This program reads a CSV file containing machine problem records and verifies the validity of each row.
If no errors are found, it flips the boolean values in the last column ("True" to "False" and vice versa)
and displays the modified dataset along with a count of changes made.

Key Features:
- Validates each row for the correct number of columns and presence of data
- Ensures the last column contains valid boolean values ("True" or "False")
- Flips all boolean values if no errors are found
- Reports errors clearly by line number and issue
- Prints the modified dataset and total number of changes

Note: The program assumes the boolean value is in the fourth column (index 3).
Big O Notation: O(n), where n is the number of rows in the CSV file.
"""

import csv

# Function: flip_booleans
# Purpose: Reads a CSV file, validates each row, flips the boolean in column 4 if valid, and prints the modified rows.
# Big O Complexity: O(n)
def flip_booleans(input_filename):
    changes_count = 0          # Tracks how many boolean values were flipped
    modified_rows = []         # Stores the header and valid data rows
    error_found = False        # Flag to determine if any errors were encountered

    # Open and read the CSV file
    with open(input_filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Extract header row
        modified_rows.append(header)

        # Validate each row
        for line_number, row in enumerate(reader, start=2):
            if len(row) != 4:
                print(f"Error in row {line_number}: Row contains missing or extra columns.")
                error_found = True
                continue

            if '' in row:
                print(f"Error in row {line_number}: Missing information in row.")
                error_found = True
                continue

            row[3] = row[3].strip().capitalize()  # Normalize boolean value

            # Validate boolean content
            if row[3] not in ['True', 'False']:
                print(f"Error in row {line_number}: Invalid boolean value '{row[3]}'.")
                error_found = True
                continue

            modified_rows.append(row)

    # If any row has errors, exit early without making changes
    if error_found:
        print("\nErrors were found in the dataset. No modifications were made.")
        return 0

    # Flip the boolean values
    for row in modified_rows[1:]:  # Skip the header
        boolean_value = row[3]
        if boolean_value == 'True':
            row[3] = 'False'
            changes_count += 1
        elif boolean_value == 'False':
            row[3] = 'True'
            changes_count += 1

    # Output the modified dataset
    print("\nModified Dataset:")
    for row in modified_rows:
        print(row)

    return changes_count

# Entry point of the program
input_filename = 'Datasets/machine_problems_dataset.csv'
changes = flip_booleans(input_filename)

if changes > 0:
    print(f"\nTotal number of changes: {changes}")
