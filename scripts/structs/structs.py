from dataclasses import dataclass


@dataclass
class Info:
    project_count: int
    job_count: int
    horizon: int
    renewable: int
    nonrenewable: int
    doubly_constrained: int

    def __str__(self):
        return f"{self.project_count:>9} | {self.job_count:>4} | {self.horizon:>7} | {self.renewable:>4} | {self.nonrenewable:>4} | {self.doubly_constrained:>4}"


@dataclass
class Resource:
    resname: str
    resavail: int
    renewable: str

    def __str__(self):
        return f"{self.resname:>10} | {self.resavail:>8} | {self.renewable}"


@dataclass
class Job:
    jobnr: int
    mode: int
    duration: int
    resources: dict
    successors: list[int]

    def __str__(self):
        return f"{self.jobnr:>3} | {self.mode:>4} | {self.duration:>8} | {self.resources} | {self.successors}"


@dataclass
class Project:
    pronr: int
    jobs_number: int
    rel_date: int
    due_date: int
    tardcost: int
    mpm_time: int
    jobs: list[Job]

    def __str__(self):
        return f"{self.pronr:>8} | {self.jobs_number:>4} | {self.rel_date:>8} | {self.due_date:>8} | {self.tardcost:>8} | {self.mpm_time:>8}"
