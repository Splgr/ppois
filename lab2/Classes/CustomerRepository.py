from abc import ABC, abstractmethod
from Customer import Customer

class CustomerRepository(ABC):
    @abstractmethod
    def get_by_id(self, customer_id) -> 'Customer': 
        pass