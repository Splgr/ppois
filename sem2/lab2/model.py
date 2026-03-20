"""
Model component for Tournament Management System
Implements data management and business logic
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple


@dataclass
class Tournament:
    """Tournament data structure"""
    id: Optional[int]
    name: str
    date: datetime
    sport: str
    winner_name: str
    prize_pool: float
    winner_earnings: float  # 60% of prize pool
    
    def __post_init__(self):
        """Calculate winner earnings automatically"""
        if self.prize_pool and not self.winner_earnings:
            self.winner_earnings = self.prize_pool * 0.6
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime('%Y-%m-%d') if isinstance(self.date, datetime) else self.date,
            'sport': self.sport,
            'winner_name': self.winner_name,
            'prize_pool': self.prize_pool,
            'winner_earnings': self.winner_earnings
        }


class TournamentModel:
    """Model for managing tournaments"""
    
    def __init__(self, database):
        self.db = database
    
    def add_tournament(self, tournament: Tournament) -> int:
        """Add new tournament to database"""
        return self.db.insert_tournament(tournament)
    
    def update_tournament(self, tournament: Tournament) -> bool:
        """Update existing tournament"""
        return self.db.update_tournament(tournament)
    
    def delete_tournament(self, tournament_id: int) -> bool:
        """Delete tournament by ID"""
        return self.db.delete_tournament(tournament_id)
    
    def get_tournament_by_id(self, tournament_id: int) -> Optional[Tournament]:
        """Get tournament by ID"""
        return self.db.get_tournament(tournament_id)
    
    def get_all_tournaments(self) -> List[Tournament]:
        """Get all tournaments"""
        return self.db.get_all_tournaments()
    
    def get_tournaments_paginated(self, page: int, page_size: int) -> Tuple[List[Tournament], int]:
        """Get tournaments with pagination"""
        return self.db.get_tournaments_paginated(page, page_size)
    
    def search_tournaments(self, criteria: dict) -> List[Tournament]:
        """Search tournaments by criteria"""
        return self.db.search_tournaments(criteria)
    
    def delete_tournaments_by_criteria(self, criteria: dict) -> int:
        """Delete tournaments by criteria, return count of deleted"""
        return self.db.delete_tournaments_by_criteria(criteria)
    
    def get_unique_sports(self) -> List[str]:
        """Get list of unique sports"""
        return self.db.get_unique_sports()
    
    def get_tournaments_count(self) -> int:
        """Get total count of tournaments"""
        return self.db.get_tournaments_count()
    
    def export_to_xml(self, filepath: str) -> bool:
        """Export all tournaments to XML file"""
        tournaments = self.get_all_tournaments()
        return self.db.export_to_xml(tournaments, filepath)
    
    def import_from_xml(self, filepath: str) -> int:
        """Import tournaments from XML file, return count of imported"""
        return self.db.import_from_xml(filepath)