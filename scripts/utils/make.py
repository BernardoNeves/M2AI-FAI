from structs import Info, Job, Project, Resource


def make_projects(data) -> list[Project]:
    projects_summary = data["projects_summary"]
    pronr = projects_summary.get("pronr", [])
    jobs = projects_summary.get("jobs", [])
    rel_date = projects_summary.get("rel_date", [])
    duedate = projects_summary.get("duedate", [])
    tardcost = projects_summary.get("tardcost", [])
    mpm_time = projects_summary.get("mpm_time", [])

    projects = []
    for p in range(len(projects_summary["pronr"])):
        project = Project(
            int(pronr[p]),
            int(jobs[p]),
            int(rel_date[p]),
            int(duedate[p]),
            int(tardcost[p]),
            int(mpm_time[p]),
            make_jobs(
                p + 1,
                data["precedence_relations"],
                data["duration_and_resources"],
                data["resource_availability"],
            ),
        )
        projects.append(project)
    return projects


def make_jobs(
    pronr: int, precedence_relations, duration_and_resources, resource_availability
) -> list[Job]:
    jobnr = precedence_relations.get("jobnr", [])
    modes = precedence_relations.get("modes", [])
    successors = precedence_relations.get("successors", [])

    duration = duration_and_resources.get("duration", [])
    rkeys = [k for k in resource_availability["resource"]]
    resources = {
        rkeys[i]: duration_and_resources.get(rkeys[i], []) for i in range(len(rkeys))
    }

    jobs = []
    for i in range(len(jobnr)):
        index = i * (pronr)
        job_resources = {}
        for r in resources:
            job_resources[r] = int(resources[r][index])
        job = Job(
            int(jobnr[index]),
            int(modes[index]),
            int(duration[index]),
            job_resources,
            list(map(int, successors[index][1:]))
            if type(successors[index]) is list
            else [int(successors[index])],
        )
        jobs.append(job)
    return jobs


def make_resources(data) -> list[Resource]:
    resources = []
    resource_names = data["resource_availability"]["resource"]
    resource_quantity = data["resource_availability"]["qty"]
    for i in range(len(resource_names)):
        rsname = (
            "renewable"
            if resource_names[i].startswith("r")
            else "nonrenewable"
            if resource_names[i].startswith("n")
            else "doubly constrained"
            if resource_names[i].startswith("d")
            else "unknown"
        )
        resource = Resource(resource_names[i], int(resource_quantity[i]), rsname)
        resources.append(resource)
    return resources


def make_info(data) -> Info:
    project_count = int(data["general_information"]["projects"])
    job_count = int(data["general_information"]["jobs_(incl_supersource/sink_)"])
    horizon = int(data["general_information"]["horizon"])
    renewable = int(data["general_information"]["renewable"])
    nonrenewable = int(data["general_information"]["nonrenewable"])
    doubly_constrained = int(data["general_information"]["doubly_constrained"])

    return Info(
        project_count,
        job_count,
        horizon,
        renewable,
        nonrenewable,
        doubly_constrained,
    )


def make_data(data) -> tuple[Info, list[Resource], list[Project]]:
    info = make_info(data)
    resources = make_resources(data)
    projects = make_projects(data)
    return info, resources, projects
