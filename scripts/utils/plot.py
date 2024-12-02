import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


def get_tables(projects, resources, solver, job_start_vars) -> tuple:
    """Generates tables for projects and resources."""
    days = int(solver.ObjectiveValue())
    schedule_table = [["Job \\ Day"] + [f"{day+1}" for day in range(days)]]
    usage_table = [["Resource \\ Day"]] + [[r.resname] for r in resources]

    for project in projects:
        columns = []
        resources_values = {}
        for job in project.jobs:
            row = ["" for _ in range(days)]
            start_day = solver.Value(job_start_vars[(project.pronr, job.jobnr)])
            for day in range(start_day, start_day + job.duration):
                if day < days:
                    for r, v in job.resources.items():
                        if r not in resources_values:
                            resources_values[r] = [0 for _ in range(days)]
                        resources_values[r][day] += int(v)
                        row[day] = f"{r} {v}"
                    if not job.resources:
                        row[day] = "N/A"
            schedule_table.append([f"{job.jobnr:>2}"] + row)
            columns.append(row)

        usage_table[0].extend([f"{day+1}" for day in range(days)])
        for i, r in enumerate(resources_values):
            usage_table[i + 1].extend(map(str, resources_values[r]))

    return schedule_table, usage_table


def plot_results(resources, projects, solver, job_start_vars):
    schedule_table, usage_table = get_tables(
        projects, resources, solver, job_start_vars
    )

    days = len(schedule_table[0]) - 1
    jobs = [row[0] for row in schedule_table[1:]]
    resources = usage_table[1:]

    job_to_color = {job: i + 1 for i, job in enumerate(jobs)}
    schedule_data = np.array(
        [
            [job_to_color[jobs[row_idx]] if cell else 0 for cell in row[1:]]
            for row_idx, row in enumerate(schedule_table[1:])
        ]
    )

    resource_data = np.array(
        [
            [int(cell) if cell.isdigit() else 0 for cell in row[1:]]
            for row in usage_table[1:]
        ]
    )

    _, axes = plt.subplots(
        2,
        1,
        figsize=(12, len(jobs) * 0.7),
        gridspec_kw={"height_ratios": [3, 1]},
    )

    cmap = plt.cm.get_cmap("tab20", len(jobs) + 1)
    cmap_colors = cmap(np.arange(len(jobs) + 1))
    cmap_colors[0] = [1, 1, 1, 1]
    custom_cmap = mcolors.ListedColormap(cmap_colors)

    axes[0].imshow(
        schedule_data, cmap=custom_cmap, aspect="auto", interpolation="nearest"
    )
    axes[0].set_xticks(range(days))
    axes[0].set_xticklabels(schedule_table[0][1:], rotation=45)
    axes[0].set_yticks(range(len(jobs)))
    axes[0].set_yticklabels(jobs)

    axes[0].set_xlabel("Days")
    axes[0].set_ylabel("Jobs")
    axes[0].set_title("Schedule")

    axes[0].set_xticks(np.arange(-0.5, days, 1), minor=True)
    axes[0].set_yticks(np.arange(-0.5, len(jobs), 1), minor=True)

    axes[0].grid(which="minor", color="black", linestyle=":", linewidth=0.5)
    axes[0].tick_params(axis="both", which="major", size=0)

    axes[1].imshow(
        resource_data, cmap="Oranges", aspect="auto", interpolation="nearest"
    )
    axes[1].set_xticks(range(days))
    axes[1].set_xticklabels(usage_table[0][1:], rotation=45)
    axes[1].set_yticks(range(len(resources)))
    axes[1].set_yticklabels([r[0] for r in resources])
    axes[1].set_xlabel("Days")
    axes[1].set_ylabel("Resources")
    axes[1].set_title("Resource Usage")

    axes[1].set_xticks(np.arange(-0.5, days, 1), minor=True)
    axes[1].set_yticks(np.arange(-0.5, len(resources), 1), minor=True)

    axes[1].grid(which="minor", color="black", linestyle=":", linewidth=0.5)
    axes[1].tick_params(axis="both", which="major", size=0)

    for i in range(len(resources)):
        for j in range(days):
            value = resource_data[i, j]
            if value > 0:
                axes[1].text(
                    j,
                    i,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=12,
                    color="black",
                    weight="bold",
                )
    plt.show()
