from mcp import Task

class Planner:
    def __init__(self):
        self.task_id = 0

    def generate_tasks(self):
        tasks = []
        for desc in ["Fetch data", "Process data", "Validate results"]:
            self.task_id += 1
            tasks.append(Task(self.task_id, desc))
        return tasks
