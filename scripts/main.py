import argparse
import os
from logging import error

from solver import solve_scheduling, tiebreaker
from utils import (
    get_file_data,
    plot_results,
    make_data,
    print_tables,
    print_makespans,
)


def solve_dataset(data):
    info, resources, projects = make_data(data)
    print_tables(info, resources, projects)

    status, solver, job_vars, solutions = solve_scheduling(
        projects, resources, info.horizon, tiebreaker
    )
    print_makespans(solutions)
    print(f"Solver status: {solver.StatusName(status)}")
    print(f"Objective value: {solver.ObjectiveValue()}")

    plot_results(resources, projects, solver, job_vars)


def main():
    os.system("cls" if os.name == "nt" else "clear")
    args = get_args()
    file_path = args.file
    save = args.save

    if not file_path or not os.path.exists(file_path):
        error("Invalid file path")
        return

    datasets = []
    if os.path.isdir(file_path):
        for root, _, files in os.walk(file_path):
            for file in files:
                if file.endswith(".txt"):
                    datasets.append(
                        (file, get_file_data(os.path.join(root, file), save))
                    )
    elif os.path.isfile(file_path) and file_path.endswith(".txt"):
        datasets.append((file_path, get_file_data(file_path, save)))

    for file, data in datasets:
        print(f"Dataset: {file}")
        solve_dataset(data)
        os.system("cls" if os.name == "nt" else "clear")

    return


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project Scheduling")
    parser.add_argument(
        "-f", "--file", help="Path to the file containing the project data"
    )
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="Save the parsed data to a JSON file",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
