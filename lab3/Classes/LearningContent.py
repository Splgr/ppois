from datetime import datetime
from exceptions import InvalidRatingException, ContentNotApprovedException

class LearningContent:
    def __init__(self, content_id: str, title: str, creator):
        self._content_id = content_id
        self._title = title
        self._creator = creator
        self._creation_date = datetime.now()
        self._ratings: list[float] = []
        self._download_count: int = 0
        self._is_approved: bool = False
    
    def add_rating(self, rating: float) -> None:
        if not (1 <= rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        self._ratings.append(rating)
    
    def get_average_rating(self) -> float:
        return sum(self._ratings) / len(self._ratings) if self._ratings else 0.0
    
    def increment_download_count(self) -> None:
        if not self._is_approved:
            raise ContentNotApprovedException("Cannot download unapproved content")
        self._download_count += 1
    
    def approve_content(self) -> None:
        self._is_approved = True
    
    def get_popularity_score(self) -> float:
        return (self._download_count * 0.6) + (len(self._ratings) * 0.4)