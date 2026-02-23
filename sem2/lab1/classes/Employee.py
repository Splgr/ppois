class Employee:
    """Персонал отеля"""
    def __init__(self, employee_id: str, name: str, role: str):
        self.id = employee_id
        self.name = name
        self.role = role
    
    def to_dict(self) -> dict:
        return {"employee_id": self.id, "name": self.name, "role": self.role}
    
    @staticmethod
    def from_dict(data: dict) -> 'Employee':
        return Employee(
            employee_id=data["employee_id"],
            name=data["name"],
            role=data["role"]
        )
    
    def __str__(self):
        return f"{self.name} ({self.role}, ID: {self.id})"
