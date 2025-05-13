from flask import Flask, render_template, request
import os
import subprocess
import sys

app = Flask(__name__)

# Mapping of program names to script paths + input simulation if needed
PROGRAMS = {
    "bubblesort": {
        "script": "python_scripts/bubblesort.py",
        "title": "Bubble Sort",
        "desc": "Sorts mobile dataset by price in ascending or descending order.",
        "dataset": "Updated_Mobile_Dataset.csv"
    },
    "flip": {
        "script": "python_scripts/flip.py",
        "title": "Flip Booleans",
        "desc": "Flips 'True' to 'False' and vice versa in machine problems dataset.",
        "dataset": "machine_problems_dataset.csv"
    },
    "stock": {
        "script": "python_scripts/stock.py",
        "title": "Stock GDP vs Population Plot",
        "desc": "Displays a scatter plot showing correlation between population and GDP growth.",
        "dataset": "Hardcoded values"
    },
    "subset_sum": {
        "script": "python_scripts/subset_sum.py",
        "title": "Subset Sum Group Selector",
        "desc": "Finds students matching score, study hours, and stress level criteria using backtracking.",
        "dataset": "Students_Grading_Dataset.csv"
    }
}

@app.route("/")
def index():
    return render_template("index.html", programs=PROGRAMS)

# Dynamic route that handles form submission for all programs
@app.route("/<program>", methods=["GET", "POST"])
def run_program(program):
    if program not in PROGRAMS:
        return "Program not found", 404

    result = {"stdout": "", "stderr": ""}

    if request.method == "POST":
        simulated_input = ""

        if program == "bubblesort":
            order = request.form.get("order", "A")
            simulated_input = f"{order}\n"

        elif program == "subset_sum":
            min_score = float(request.form.get("min_score", 70))
            max_score = float(request.form.get("max_score", 90))
            min_study_hours = float(request.form.get("min_study_hours", 10))
            max_study_hours = float(request.form.get("max_study_hours", 20))
            stress_level = int(request.form.get("stress_level", 5))
            num_students = int(request.form.get("num_students", 5))

            simulated_input = f"{min_score}\n{max_score}\n{min_study_hours}\n{max_study_hours}\n{stress_level}\n{num_students}\nno\n"

        try:
            proc = subprocess.run(
                [sys.executable, PROGRAMS[program]["script"]],
                input=simulated_input,
                capture_output=True,
                text=True,
                timeout=120
            )
            result["stdout"] = proc.stdout
            result["stderr"] = proc.stderr
        except subprocess.TimeoutExpired:
            result["stderr"] = "Error: Program took too long to execute."

    return render_template(f"{program}.html", program=PROGRAMS[program], result=result)

if __name__ == "__main__":
    app.run(debug=True)