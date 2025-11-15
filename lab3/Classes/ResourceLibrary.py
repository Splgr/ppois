from typing import List
from learning_resource import LearningResource
from exceptions import ContentNotFoundException

class ResourceLibrary:
    def __init__(self):
        self._resources: List[LearningResource] = []
    
    def add_resource(self, resource: LearningResource) -> None:
        self._resources.append(resource)
    
    def search_resources(self, query: str) -> List[LearningResource]:
        results = []
        for resource in self._resources:
            if (query.lower() in resource._title.lower() or 
                query.lower() in resource._description.lower()):
                results.append(resource)
        return results
    
    def get_resource_count(self) -> int:
        return len(self._resources)
    
    def get_resource_by_title(self, title: str) -> LearningResource:
        for resource in self._resources:
            if resource._title == title:
                return resource
        raise ContentNotFoundException(f"Resource with title '{title}' not found")