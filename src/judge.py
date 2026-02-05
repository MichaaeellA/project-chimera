class Judge:
    def validate(self, task):
        print(f"Judge validating task {task.id}")
        if task.description == "Process data":
            print("HITL escalation required!")
        else:
            print("Task approved.")
