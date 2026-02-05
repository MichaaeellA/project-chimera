from planner import Planner
from worker import Worker
from judge import Judge

planner = Planner()
worker = Worker()
judge = Judge()

tasks = planner.generate_tasks()

for task in tasks:
    task = worker.execute(task)
    judge.validate(task)
