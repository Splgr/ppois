from typing import Optional
from exceptions import InsufficientPermissionsException, ContentNotFoundException

class Poll:
    def __init__(self, question: str):
        self._question = question
        self._options: list[str] = []
        self._votes: dict[str, int] = {}
        self._is_active: bool = True
    
    def add_option(self, option: str) -> None:
        if option not in self._options:
            self._options.append(option)
            self._votes[option] = 0
    
    def vote(self, option: str) -> bool:
        if not self._is_active:
            raise InsufficientPermissionsException("Poll is no longer active")
        
        if option not in self._options:
            raise ContentNotFoundException("Option not found in poll")
        
        self._votes[option] += 1
        return True
    
    def get_results(self) -> dict[str, int]:
        return self._votes.copy()
    
    def get_winner(self) -> Optional[str]:
        if not self._votes:
            return None
        return max(self._votes.items(), key=lambda x: x[1])[0]