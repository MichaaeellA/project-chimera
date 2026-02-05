class Worker:
    def execute(self, task):
        print(f"Worker executing task {task.id}: {task.description}")
        task.result = f"{task.description} done"
        task.status = "completed"
        return task
