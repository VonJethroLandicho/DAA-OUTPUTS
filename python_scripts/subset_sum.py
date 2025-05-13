# Import necessary libraries: pandas for data handling, matplotlib for plotting, tqdm for progress, sys for input handling, os for path operations.

# Function to load and clean the dataset:
# - Reads CSV file.
# - Checks for missing values in critical columns.
# - Prompts user to continue or exit if missing values are found.
# - Allows excluding rows with missing critical data.
# - Asks user to choose a row range for analysis or uses a default range if run via Flask.

# Function to find the best student group:
# - Filters data based on score, study hours, and stress level criteria.
# - Sorts students by score in descending order.
# - Uses iterative backtracking (via a stack) to find all possible valid groups of the specified size.
# - Returns the first valid group found or None if no group matches.

# Function to display the results:
# - Prints student data in a readable format.
# - Plots a grouped bar chart showing Total Score, Study Hours, and Stress Level.
# - Displays a table of additional student information below the chart.

# Main function:
# - Loads dataset.
# - Collects filter criteria (either interactively or uses defaults in non-interactive environments).
# - Calls function to find a matching group of students.
# - Displays results.
# - Offers to rerun the program if in interactive mode.

# Entry point to run the script when executed directly.
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys  # Needed for input simulation check
import os

def load_data(file_name):
    try:
        data = pd.read_csv(file_name)
        print("Verifying CSV file...")
        
        # Check for missing data only in critical columns
        critical_columns = ['First_Name', 'Last_Name', 'Stress_Level', 'Study_Hours_per_Week', 'Total_Score', 'Student_ID']
        missing_columns = data[critical_columns].isnull().sum()
        missing_rows = data[critical_columns].isnull().any(axis=1)

        if missing_columns.any():
            print("\nMissing information in the following columns:")
            for column, missing_count in missing_columns[missing_columns > 0].items():
                print(f"- {column}: {missing_count} missing value(s)")
            print("\nRows with missing information:")
            for idx in data[missing_rows].index:
                missing_in_row = data.columns[data.iloc[idx].isnull()]
                print(f"Row {idx + 1} has missing information in the following columns: {', '.join(missing_in_row)}")
            
            while True:
                continue_prompt = input("Would you like to continue? (yes/no): ").strip().lower() if sys.stdin.isatty() else "yes"
                if continue_prompt == 'no':
                    print("Exiting program due to missing information.")
                    exit()
                elif continue_prompt == 'yes':
                    rows_to_exclude = data[
                        data['Study_Hours_per_Week'].isnull() |
                        data['Total_Score'].isnull() |
                        data['Stress_Level'].isnull() |
                        data['First_Name'].isnull() |
                        data['Last_Name'].isnull() |
                        data['Student_ID'].isnull()
                    ]
                    excluded_count = len(rows_to_exclude)
                    data = data.dropna(subset=critical_columns)
                    if excluded_count > 0:
                        print(f"\n{excluded_count} rows have been excluded due to missing required information.")
                    else:
                        print("\nNo students were excluded.")
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
        
        # Select a range of rows for processing
        print("\nSelect the range of rows for the backtracking algorithm:")
        print("1. 1 to 500")
        print("2. 501 to 1000")
        print("3. 1001 to 1500")
        print("4. 1501 to 2000")
        print("5. 2001 to 2500")
        print("6. 2501 to 3000")
        print("7. 3001 to 3500")
        print("8. 3501 to 4000")
        print("9. 4001 to 4500")
        print("10. 4501 to 5000")

        while True:
            if sys.stdin.isatty():
                choice = int(input("Enter your choice (1-10): "))
                if 1 <= choice <= 10:
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 10.")
            else:
                # Running via Flask – use default row range
                print("Using default row range: 1–500")
                choice = 1  # Default for Flask
                break

        row_ranges = {
            1: (0, 500),
            2: (500, 1000),
            3: (1000, 1500),
            4: (1500, 2000),
            5: (2000, 2500),
            6: (2500, 3000),
            7: (3000, 3500),
            8: (3500, 4000),
            9: (4000, 4500),
            10: (4500, 5000),
        }
        start, end = row_ranges.get(choice, (0, 500))
        data = data.iloc[start:end]
        print(f"Selected rows from {start+1} to {end} for processing.")

        return data

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def find_best_group(data, min_score, max_score, min_study_hours, max_study_hours, stress_level, num_students):
    data['Full_Name'] = data['First_Name'] + ' ' + data['Last_Name']
    filtered_data = data[(
        (data['Total_Score'] >= min_score) &
        (data['Total_Score'] <= max_score) &
        (data['Study_Hours_per_Week'] >= min_study_hours) &
        (data['Study_Hours_per_Week'] <= max_study_hours) &
        (data['Stress_Level'] <= stress_level)
    )]

    # Sort by score descending
    filtered_data = filtered_data.sort_values(by='Total_Score', ascending=False)

    results = []
    print("Processing... Please wait while the best group is being selected.")

    # Use stack for iterative backtracking
    stack = [(0, [])]  # (index, selected_students)
    while stack:
        index, selected = stack.pop()

        if len(selected) == num_students:
            results.append(selected)
            continue

        if index >= len(filtered_data) or len(selected) > num_students:
            continue

        student = filtered_data.iloc[index]

        # Option: include current student
        if (
            min_score <= student['Total_Score'] <= max_score and
            min_study_hours <= student['Study_Hours_per_Week'] <= max_study_hours and
            student['Stress_Level'] <= stress_level
        ):
            stack.append((index + 1, selected + [student]))

        # Option: skip current student
        stack.append((index + 1, selected))

    return pd.DataFrame(results[0]) if results else None

def display_results(group):
    if group is None or group.empty:
        print("\nNo matching students found.")
        return

    print("\nSolution Found! Displaying the selected students...\n")
    print(group[['Student_ID', 'Full_Name', 'Email', 'Gender', 'Age', 'Department', 'Total_Score', 'Study_Hours_per_Week', 'Stress_Level']])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})
    bar_width = 0.25
    index = range(len(group))

    bars_score = ax1.bar(index, group['Total_Score'], bar_width, label='Total Score', color='skyblue')
    bars_study_hours = ax1.bar([i + bar_width for i in index], group['Study_Hours_per_Week'], bar_width, label='Study Hours', color='lightgreen')
    bars_stress_level = ax1.bar([i + 2 * bar_width for i in index], group['Stress_Level'], bar_width, label='Stress Level', color='lightcoral')

    for i in range(len(group)):
        ax1.text(index[i], bars_score[i].get_height() / 2, f'{group["Total_Score"].iloc[i]:.1f}',
                 ha='center', va='center', color='black', fontsize=10)
        ax1.text(index[i] + bar_width, bars_study_hours[i].get_height() / 2, f'{group["Study_Hours_per_Week"].iloc[i]:.1f}',
                 ha='center', va='center', color='black', fontsize=10)
        ax1.text(index[i] + 2 * bar_width, bars_stress_level[i].get_height() / 2, f'{group["Stress_Level"].iloc[i]:.1f}',
                 ha='center', va='center', color='black', fontsize=10)

    ax1.set_ylabel('Scores / Hours / Stress')
    ax1.set_title('Scores, Study Hours, and Stress Levels of Selected Students')
    ax1.set_xticks([i + bar_width for i in index])
    ax1.set_xticklabels(group['Full_Name'], rotation=45, ha="right")
    ax1.legend()

    ax2.axis('tight')
    ax2.axis('off')
    table_data = group[['Student_ID', 'Full_Name', 'Email', 'Gender', 'Age', 'Department']].values
    column_labels = ['Student_ID', 'Full_Name', 'Email', 'Gender', 'Age', 'Department']
    table = ax2.table(cellText=table_data, colLabels=column_labels, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    ax2.set_title("Additional information on the students", fontsize=14, loc='center', pad=20)

    plt.tight_layout()
    plt.show()

def main():
    file_path = os.path.join('Datasets', 'Students_Grading_Dataset.csv')
    data = load_data(file_path)

    while True:
        try:
            if sys.stdin.isatty():
                while True:
                    try:
                        min_score = float(input("Enter minimum total score: "))
                        max_score = float(input("Enter maximum total score: "))
                        if min_score > max_score:
                            print("Minimum score should not be greater than maximum score.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                while True:
                    try:
                        min_study_hours = float(input("Enter minimum study hours per week: "))
                        max_study_hours = float(input("Enter maximum study hours per week: "))
                        if min_study_hours > max_study_hours:
                            print("Minimum study hours should not be greater than maximum study hours.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                stress_level = int(input("Enter maximum stress level (1-10): "))
                while stress_level < 1 or stress_level > 10:
                    print("Stress level must be between 1 and 10.")
                    stress_level = int(input("Enter maximum stress level (1-10): "))

                while True:
                    try:
                        num_students = int(input("Enter the number of students required for the group (Maximum 50): "))
                        if num_students <= 0:
                            print("Number of students must be greater than 0.")
                        elif num_students > 50:
                            print("Number of students cannot exceed 50.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            else:
                # Simulated defaults when running via Flask
                print("Using default input values for demonstration purposes.")
                min_score = 70
                max_score = 90
                min_study_hours = 10
                max_study_hours = 20
                stress_level = 5
                num_students = 5

            print(f"\nFinding group with:\nMin Score: {min_score}\nMax Score: {max_score}")
            print(f"Min Study Hours: {min_study_hours}\nMax Study Hours: {max_study_hours}")
            print(f"Max Stress Level: {stress_level}\nRequired Students: {num_students}")

            group = find_best_group(data, min_score, max_score, min_study_hours, max_study_hours, stress_level, num_students)
            display_results(group)

            if sys.stdin.isatty():
                again = input("\nDo you want to run the program again? (yes/no): ").strip().lower()
            else:
                again = "no"

            if again != 'yes':
                break

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()