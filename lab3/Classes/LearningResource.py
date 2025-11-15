from typing import Optional
from User import User

class LearningResource:
    def __init__(self, title: str, resource_type: str):
        self._title = title
        self._resource_type = resource_type
        self._description: str = ""
        self._uploader: Optional[User] = None
        self._download_count: int = 0
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def set_uploader(self, uploader: User) -> None:
        self._uploader = uploader
    
    def increment_download_count(self) -> None:
        self._download_count += 1
    
    def get_resource_info(self) -> dict:
        return {
            "title": self._title,
            "type": self._resource_type,
            "uploader": self._uploader.username if self._uploader else "Unknown",
            "downloads": self._download_count
        }