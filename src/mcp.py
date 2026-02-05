class Task:
    def __init__(self, id, description, status="pending", result=None):
        self.id = id
        self.description = description
        self.status = status
        self.result = result

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "result": self.result
        }
