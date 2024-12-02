from tabulate import tabulate

from structs import Info, Project, Resource


def print_info(info: Info):
    info_table = [["Projects", "Jobs", "Horizon", "RN_R", "NR_R", "DC_R"]]
    info_table.append(
        list(
            map(
                str,
                [
                    info.project_count,
                    info.job_count,
                    info.horizon,
                    info.renewable,
                    info.nonrenewable,
                    info.doubly_constrained,
                ],
            )
        )
    )
    print_tabulate("General Information", info_table)


def print_resources(resources: list[Resource]):
    resources_table = [["Resource", "Quantity", "Renewable"]]
    for resource in resources:
        resources_table.append(
            list(map(str, [resource.resname, resource.resavail, resource.renewable]))
        )
    print_tabulate("Resource Availability", resources_table)


def print_projects(projects: list[Project]):
    projects_table = [
        ["Project", "Jobs", "Rel Date", "Due Date", "Tardcost", "MPM Time"]
    ]
    jobs_header = ["Job", "Mode", "Duration", "Resources", "Successors"]
    jobs_table = []
    for project in projects:
        projects_table.append(
            list(
                map(
                    str,
                    [
                        project.pronr,
                        project.jobs_number,
                        project.rel_date,
                        project.due_date,
                        project.tardcost,
                        project.mpm_time,
                    ],
                )
            )
        )
        p_jobs_table = [jobs_header]
        for job in project.jobs:
            p_jobs_table.append(
                list(
                    map(
                        str,
                        [
                            job.jobnr,
                            job.mode,
                            job.duration,
                            job.resources,
                            job.successors,
                        ],
                    )
                )
            )
        jobs_table.append(p_jobs_table)

    print_tabulate("Project Information", projects_table)


def print_makespans(solutions: list[tuple[str, int]]):
    table = [[f"Solution n / {len(solutions)} ", "Makespan"]] + [
        list(map(str, [i + 1, makespan])) for i, (_, makespan) in enumerate(solutions)
    ]
    print_tabulate("Makespans", table)


def print_tables(info: Info, resources: list[Resource], projects: list[Project]):
    print_info(info)
    print_resources(resources)
    print_projects(projects)

def print_tabulate(title: str, table: list):
    """Prints a table in a formatted style."""
    print(f"\t{title}\n{tabulate(table, headers='firstrow', tablefmt='fancy_grid')}\n")
