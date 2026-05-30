from Course import Course
from User import User
from ForumThread import ForumThread
from exceptions import InsufficientPermissionsException

class DiscussionForum:
    def __init__(self, course: Course):
        self._course = course
        self._threads: list[ForumThread] = []
    
    def create_thread(self, author: User, title: str) -> ForumThread:
        if author not in self._course._current_students and author != self._course._instructor:
            raise InsufficientPermissionsException("Only enrolled students and instructors can create threads")
        
        thread = ForumThread(author, title)
        self._threads.append(thread)
        return thread
    
    def get_thread_count(self) -> int:
        return len(self._threads)
    
    def search_threads(self, query: str) -> list[ForumThread]:
        return [thread for thread in self._threads 
                if query.lower() in thread._title.lower()]