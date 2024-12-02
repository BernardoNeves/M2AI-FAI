"""
This is a form of a flexible job shop scheduling
This problem can include different types of constraints:
    - Hard constraints: mandatory to get a vaId solution
    - Soft constraints: prefered but not strictly required.
        so can be violated under certain circumstances

Hard constraints:
    -Job precendence - a job can only start after all its predecessors have finished
    -Resources capacity:
        - do not use more resources than available
        - renewable: resources are replenished, capacity per day
        - nonrenewable: resources are not replenished, capacity is for all days
    -Project deadline:
        - some projects have a deadline

More constraints can be added to make this problem more realistic:
    - limit the duration of the whole multi-project schedule (hard)
    - minimize the duration (makespan) of each project (soft)
"""

from ortools.sat.python import cp_model
from structs import Project, Resource


class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, projects, job_start_vars, job_end_vars):
        super().__init__()
        self.projects = projects
        self.job_start_vars = job_start_vars
        self.job_end_vars = job_end_vars
        self.solutions = []

    def on_solution_callback(self):
        solution = {}
        makespan_value = 0

        for project in self.projects:
            for job in project.jobs:
                start = self.Value(self.job_start_vars[(project.pronr, job.jobnr)])
                end = self.Value(self.job_end_vars[(project.pronr, job.jobnr)])
                solution[(project.pronr, job.jobnr)] = (start, end)
                makespan_value = max(makespan_value, end)

        self.solutions.append((solution, makespan_value))


def create_job_variables(model, projects, horizon):
    job_start_vars, job_end_vars, job_intervals = {}, {}, {}

    for project in projects:
        for job in project.jobs:
            start, end, interval = create_job_for_project(model, job, project, horizon)
            job_start_vars[(project.pronr, job.jobnr)] = start
            job_end_vars[(project.pronr, job.jobnr)] = end
            job_intervals[(project.pronr, job.jobnr)] = interval

    return job_start_vars, job_end_vars, job_intervals


def create_job_for_project(model, job, project, horizon):
    start = model.NewIntVar(0, horizon, f"s_p{project.pronr}_j{job.jobnr}")
    end = model.NewIntVar(0, horizon, f"e_p{project.pronr}_j{job.jobnr}")
    interval = model.NewIntervalVar(
        start, job.duration, end, f"i_p{project.pronr}_j{job.jobnr}"
    )
    return start, end, interval


def add_precedence_constraints(model, projects, job_start_vars, job_end_vars):
    for project in projects:
        for job in project.jobs:
            for successor in job.successors:
                if successor != 0:
                    model.Add(
                        job_start_vars[(project.pronr, successor)]
                        >= job_end_vars[(project.pronr, job.jobnr)]
                    )


def add_resource_constraints(model, projects, resources, job_intervals):
    for resource in resources:
        if resource.renewable == "renewable":
            intervals, demands = [], []
            for project in projects:
                for job in project.jobs:
                    demands.append(job.resources[resource.resname])
                    intervals.append(job_intervals[(project.pronr, job.jobnr)])
            model.AddCumulative(intervals, demands, resource.resavail)


def add_makespan_objective(model, projects, job_end_vars, horizon):
    makespan = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(
        makespan,
        [
            job_end_vars[(project.pronr, job.jobnr)]
            for project in projects
            for job in project.jobs
        ],
    )
    model.Minimize(makespan)
    return makespan


def solve_scheduling(
    projects: list[Project], resources: list[Resource], horizon: int, tiebreaker=None
):
    model = cp_model.CpModel()
    job_starts, job_ends, job_intervals = create_job_variables(model, projects, horizon)
    add_precedence_constraints(model, projects, job_starts, job_ends)
    add_resource_constraints(model, projects, resources, job_intervals)
    add_makespan_objective(model, projects, job_ends, horizon)

    solver = cp_model.CpSolver()
    collector = SolutionCollector(projects, job_starts, job_ends)
    status = solver.SolveWithSolutionCallback(model, collector)
    # status = solver.Solve(model)

    if tiebreaker and len(set([m for _, m in collector.solutions])) < len(
        collector.solutions
    ):
        print("Tied makespan values found, applying tiebreaker.")
        collector.solutions.sort(key=lambda x: (x[1], tiebreaker(x[0])))

    return status, solver, job_starts, collector.solutions


def tiebreaker(solution):
    return sum(start for start, _ in solution.values())
