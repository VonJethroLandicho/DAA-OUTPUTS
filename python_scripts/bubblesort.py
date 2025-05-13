"""
Mobile Dataset Sorting Script

Description:
-------------
This script processes and sorts a mobile phone dataset stored in a CSV file using the Bubble Sort algorithm.
The dataset is validated to ensure key fields are populated and numeric where appropriate (especially the "Price" field).
Users can choose whether to sort the dataset in ascending or descending order based on the "Price" column.
The sorted data is then saved into a new CSV file, and any rows with invalid or missing data are reported.

Main Functionalities:
---------------------
- Read and validate data from a CSV file.
- Identify and report invalid/missing entries.
- Sort valid data using the Bubble Sort algorithm.
- Allow user to choose sorting order (ascending/descending).
- Write the sorted dataset to a new CSV file.
- Display processing time and warnings for skipped rows.

Intended Use:
-------------
This script is best suited for educational purposes or small datasets due to the inefficiency of Bubble Sort for large data volumes.
"""
import csv
import os
import time
import sys  # Needed for input simulation check

# Function to perform Bubble Sort on the dataset based on a specific column
def bubble_sort(data, key_index, ascending=True):
    n = len(data)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if (ascending and float(data[j][key_index]) > float(data[j + 1][key_index])) or \
               (not ascending and float(data[j][key_index]) < float(data[j + 1][key_index])):
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

# Function to read the CSV file and return its content as a list
def read_csv(filename):
    try:
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit()

# Function to write sorted data back to a CSV file
def write_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Function to format elapsed time into a readable format (minutes and seconds)
def format_time(seconds):
    minutes = int(seconds) // 60
    remaining_seconds = int(seconds) % 60
    return f"{minutes}:{remaining_seconds:02d} ({minutes * 60 + remaining_seconds} seconds)"

# Main function to execute the sorting process
def main():
    # Define the input CSV file name
    input_file = os.path.join("Datasets", "Updated_Mobile_Dataset.csv")

    # Read data from the CSV file
    data = read_csv(input_file)
    if not data:
        print("Error: CSV file is empty or could not be read.")
        return

    # Extract the header and the data rows
    header, rows = data[0], data[1:]

    # Find the index of the "Price" column
    try:
        price_column = header.index("Price")
    except ValueError:
        print("Error: 'Price' column not found in CSV header.")
        return

    # Define the required columns and check for missing fields
    required_columns = ["Number", "Model", "Company", "Price", "Rating", "No_of_ratings", "TotalReviews", "RamSize", "RomSize"]
    missing_column_indexes = {col: header.index(col) for col in required_columns if col in header}

    valid_rows = []  # List to store valid data rows
    invalid_rows = []  # List to store invalid data rows

    # Validate data rows and separate invalid entries
    for i, row in enumerate(rows, start=2):  
        missing_fields = [col for col, idx in missing_column_indexes.items() if not row[idx].strip()]
        if missing_fields:
            invalid_rows.append((i, missing_fields))
            continue
        try:
            float(row[price_column])  # Ensure the "Price" column contains valid numbers
            valid_rows.append(row)
        except ValueError:
            invalid_rows.append((i, ["Price"]))

    # Prompt user for sorting order
    while True:
        if sys.stdin.isatty():
            # Running in terminal — wait for user input
            order = input("Press 'A' for ascending or 'D' for descending order: ").strip().upper()
        else:
            # Running via Flask — use default value
            order = 'A'
            print("Using default sorting order: Ascending")

        if order in ('A', 'D'):
            break
        print("Invalid input! Choose only between A (Ascending) or D (Descending).")

    ascending = order == 'A'  # Determine sorting direction

    print("Processing...")
    start_time = time.time()  # Record start time

    # Perform Bubble Sort on valid data
    sorted_data = bubble_sort(valid_rows, price_column, ascending)

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time

    # Add header back to sorted data
    sorted_data.insert(0, header)

    # Define output file name based on sorting order
    output_file = os.path.join("Datasets", "Sorted_Mobile_Dataset_Ascending.csv" if ascending else "Sorted_Mobile_Dataset_Descending.csv")

    # Write sorted data to a new CSV file
    write_csv(output_file, sorted_data)

    print(f"Sorted dataset saved to {os.path.abspath(output_file)}")
    print(f"Sorting completed in {format_time(elapsed_time)}")

    # Display warning for skipped invalid rows
    if invalid_rows:
        print("Warning: The following rows contained errors and were skipped:")
        for row_num, columns in invalid_rows:
            print(f"Row {row_num}: Missing or invalid data in {', '.join(columns)}")

    # Inform user about Bubble Sort efficiency
    print("\nSince this program uses bubble sort (an algorithm usually used for small data sets),\n"
          "it takes some time in sorting large amounts of data. Thank you for your patience!")

if __name__ == "__main__":
    main()