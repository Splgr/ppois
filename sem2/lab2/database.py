"""
Database handler for Tournament Management System
Uses SQLite for storage
"""
import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple
from model import Tournament


class Database:
    """SQLite database handler"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create database tables"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                sport TEXT NOT NULL,
                winner_name TEXT NOT NULL,
                prize_pool REAL NOT NULL,
                winner_earnings REAL NOT NULL
            )
        ''')
        self.conn.commit()
    
    def insert_tournament(self, tournament: Tournament) -> int:
        """Insert new tournament"""
        self.cursor.execute('''
            INSERT INTO tournaments (name, date, sport, winner_name, prize_pool, winner_earnings)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            tournament.name,
            tournament.date.strftime('%Y-%m-%d') if isinstance(tournament.date, datetime) else tournament.date,
            tournament.sport,
            tournament.winner_name,
            tournament.prize_pool,
            tournament.winner_earnings
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_tournament(self, tournament: Tournament) -> bool:
        """Update tournament"""
        self.cursor.execute('''
            UPDATE tournaments
            SET name=?, date=?, sport=?, winner_name=?, prize_pool=?, winner_earnings=?
            WHERE id=?
        ''', (
            tournament.name,
            tournament.date.strftime('%Y-%m-%d') if isinstance(tournament.date, datetime) else tournament.date,
            tournament.sport,
            tournament.winner_name,
            tournament.prize_pool,
            tournament.winner_earnings,
            tournament.id
        ))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_tournament(self, tournament_id: int) -> bool:
        """Delete tournament by ID"""
        self.cursor.execute('DELETE FROM tournaments WHERE id=?', (tournament_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_tournament(self, tournament_id: int) -> Optional[Tournament]:
        """Get tournament by ID"""
        self.cursor.execute('SELECT * FROM tournaments WHERE id=?', (tournament_id,))
        row = self.cursor.fetchone()
        if row:
            return self._row_to_tournament(row)
        return None
    
    def get_all_tournaments(self) -> List[Tournament]:
        """Get all tournaments"""
        self.cursor.execute('SELECT * FROM tournaments ORDER BY date DESC')
        rows = self.cursor.fetchall()
        return [self._row_to_tournament(row) for row in rows]
    
    def get_tournaments_paginated(self, page: int, page_size: int) -> Tuple[List[Tournament], int]:
        """Get tournaments with pagination"""
        offset = (page - 1) * page_size
        
        # Get total count
        self.cursor.execute('SELECT COUNT(*) FROM tournaments')
        total = self.cursor.fetchone()[0]
        
        # Get page data
        self.cursor.execute('''
            SELECT * FROM tournaments 
            ORDER BY date DESC 
            LIMIT ? OFFSET ?
        ''', (page_size, offset))
        
        rows = self.cursor.fetchall()
        tournaments = [self._row_to_tournament(row) for row in rows]
        
        return tournaments, total
    
    def search_tournaments(self, criteria: dict) -> List[Tournament]:
        """Search tournaments by various criteria"""
        query = "SELECT * FROM tournaments WHERE 1=1"
        params = []
        
        # Search by tournament name or date
        if criteria.get('name_or_date'):
            search_term = f"%{criteria['name_or_date']}%"
            query += " AND (name LIKE ? OR date LIKE ?)"
            params.extend([search_term, search_term])
        
        # Search by sport
        if criteria.get('sport'):
            query += " AND sport = ?"
            params.append(criteria['sport'])
        
        # Search by winner name (can be partial - just first name)
        if criteria.get('winner_name'):
            search_term = f"%{criteria['winner_name']}%"
            query += " AND winner_name LIKE ?"
            params.append(search_term)
        
        # Search by prize pool range
        if criteria.get('prize_min') is not None:
            query += " AND prize_pool >= ?"
            params.append(criteria['prize_min'])
        
        if criteria.get('prize_max') is not None:
            query += " AND prize_pool <= ?"
            params.append(criteria['prize_max'])
        
        # Search by winner earnings range
        if criteria.get('earnings_min') is not None:
            query += " AND winner_earnings >= ?"
            params.append(criteria['earnings_min'])
        
        if criteria.get('earnings_max') is not None:
            query += " AND winner_earnings <= ?"
            params.append(criteria['earnings_max'])
        
        query += " ORDER BY date DESC"
        
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [self._row_to_tournament(row) for row in rows]
    
    def delete_tournaments_by_criteria(self, criteria: dict) -> int:
        """Delete tournaments by criteria, return count of deleted"""
        query = "DELETE FROM tournaments WHERE 1=1"
        params = []
        
        # Delete by tournament name or date
        if criteria.get('name_or_date'):
            search_term = f"%{criteria['name_or_date']}%"
            query += " AND (name LIKE ? OR date LIKE ?)"
            params.extend([search_term, search_term])
        
        # Delete by sport
        if criteria.get('sport'):
            query += " AND sport = ?"
            params.append(criteria['sport'])
        
        # Delete by winner name
        if criteria.get('winner_name'):
            search_term = f"%{criteria['winner_name']}%"
            query += " AND winner_name LIKE ?"
            params.append(search_term)
        
        # Delete by prize pool range
        if criteria.get('prize_min') is not None:
            query += " AND prize_pool >= ?"
            params.append(criteria['prize_min'])
        
        if criteria.get('prize_max') is not None:
            query += " AND prize_pool <= ?"
            params.append(criteria['prize_max'])
        
        # Delete by winner earnings range
        if criteria.get('earnings_min') is not None:
            query += " AND winner_earnings >= ?"
            params.append(criteria['earnings_min'])
        
        if criteria.get('earnings_max') is not None:
            query += " AND winner_earnings <= ?"
            params.append(criteria['earnings_max'])
        
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.rowcount
    
    def get_unique_sports(self) -> List[str]:
        """Get list of unique sports"""
        self.cursor.execute('SELECT DISTINCT sport FROM tournaments ORDER BY sport')
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
    
    def get_tournaments_count(self) -> int:
        """Get total count of tournaments"""
        self.cursor.execute('SELECT COUNT(*) FROM tournaments')
        return self.cursor.fetchone()[0]
    
    def _row_to_tournament(self, row) -> Tournament:
        """Convert database row to Tournament object"""
        return Tournament(
            id=row['id'],
            name=row['name'],
            date=datetime.strptime(row['date'], '%Y-%m-%d'),
            sport=row['sport'],
            winner_name=row['winner_name'],
            prize_pool=row['prize_pool'],
            winner_earnings=row['winner_earnings']
        )
    
    def export_to_xml(self, tournaments: List[Tournament], filepath: str) -> bool:
        """Export tournaments to XML file using DOM parser"""
        try:
            from xml.dom.minidom import Document
            
            doc = Document()
            root = doc.createElement('tournaments')
            doc.appendChild(root)
            
            for tournament in tournaments:
                tour_elem = doc.createElement('tournament')
                tour_elem.setAttribute('id', str(tournament.id))
                
                name_elem = doc.createElement('name')
                name_elem.appendChild(doc.createTextNode(tournament.name))
                tour_elem.appendChild(name_elem)
                
                date_elem = doc.createElement('date')
                date_elem.appendChild(doc.createTextNode(
                    tournament.date.strftime('%Y-%m-%d') if isinstance(tournament.date, datetime) else tournament.date
                ))
                tour_elem.appendChild(date_elem)
                
                sport_elem = doc.createElement('sport')
                sport_elem.appendChild(doc.createTextNode(tournament.sport))
                tour_elem.appendChild(sport_elem)
                
                winner_elem = doc.createElement('winner_name')
                winner_elem.appendChild(doc.createTextNode(tournament.winner_name))
                tour_elem.appendChild(winner_elem)
                
                prize_elem = doc.createElement('prize_pool')
                prize_elem.setAttribute('value', str(tournament.prize_pool))
                tour_elem.appendChild(prize_elem)
                
                earnings_elem = doc.createElement('winner_earnings')
                earnings_elem.setAttribute('value', str(tournament.winner_earnings))
                tour_elem.appendChild(earnings_elem)
                
                root.appendChild(tour_elem)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                doc.writexml(f, indent='  ', addindent='  ', newl='\n', encoding='utf-8')
            
            return True
        except Exception as e:
            print(f"Error exporting to XML: {e}")
            return False
    
    def import_from_xml(self, filepath: str) -> int:
        """Import tournaments from XML file using SAX parser"""
        try:
            import xml.sax
            from xml.sax.handler import ContentHandler
            
            class TournamentHandler(ContentHandler):
                def __init__(self):
                    self.tournaments = []
                    self.current_tournament = {}
                    self.current_element = ""
                    self.current_text = ""
                
                def startElement(self, name, attrs):
                    self.current_element = name
                    self.current_text = ""
                    
                    if name == "tournament":
                        self.current_tournament = {'id': int(attrs.get('id', 0))}
                    
                    elif name == "prize_pool":
                        self.current_tournament['prize_pool'] = float(attrs.get('value', 0))
                    
                    elif name == "winner_earnings":
                        self.current_tournament['winner_earnings'] = float(attrs.get('value', 0))
                
                def endElement(self, name):
                    if name in ['name', 'date', 'sport', 'winner_name']:
                        self.current_tournament[name] = self.current_text.strip()
                    
                    elif name == 'tournament':
                        self.tournaments.append(self.current_tournament)
                
                def characters(self, content):
                    self.current_text += content
            
            handler = TournamentHandler()
            parser = xml.sax.make_parser()
            parser.setContentHandler(handler)
            parser.parse(filepath)
            
            # Insert imported tournaments (ПРОВЕРКА НА ДУБЛИКАТЫ)
            count = 0
            duplicates = 0
            
            for tour_data in handler.tournaments:
                # Проверяем, есть ли уже такой турнир (по названию + дате)
                self.cursor.execute('''
                    SELECT id FROM tournaments 
                    WHERE name = ? AND date = ?
                ''', (tour_data['name'], tour_data['date']))
                
                if self.cursor.fetchone():
                    duplicates += 1
                    print(f"⚠️ Пропущен дубликат: {tour_data['name']} ({tour_data['date']})")
                    continue
                
                tournament = Tournament(
                    id=None,
                    name=tour_data['name'],
                    date=datetime.strptime(tour_data['date'], '%Y-%m-%d'),
                    sport=tour_data['sport'],
                    winner_name=tour_data['winner_name'],
                    prize_pool=tour_data['prize_pool'],
                    winner_earnings=tour_data['winner_earnings']
                )
                self.insert_tournament(tournament)
                count += 1
            
            if duplicates > 0:
                print(f"✅ Импортировано: {count}, Пропущено дубликатов: {duplicates}")
            
            return count
        
        except Exception as e:
            print(f"Error importing from XML: {e}")
            return 0
    
    def close(self):
        """Close database connection"""
        self.conn.close()