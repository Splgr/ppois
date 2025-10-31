class Customer:
    def __init__(
        self,
        name: str,
        address: str,
        email: str,
        phone: str,
        budget: float
    ):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.budget = budget