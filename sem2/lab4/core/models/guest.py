class Guest:
    """Гость отеля"""
    def __init__(self, guest_id: str, name: str, contact: str):
        self.id = guest_id
        self.name = name
        self.contact = contact
    
    def to_dict(self) -> dict:
        return {"guest_id": self.id, "name": self.name, "contact": self.contact}
    
    @staticmethod
    def from_dict(data: dict) -> 'Guest':
        return Guest(
            guest_id=data["guest_id"],
            name=data["name"],
            contact=data["contact"]
        )
    
    def __str__(self):
        return f"{self.name} (ID: {self.id}, тел: {self.contact})"