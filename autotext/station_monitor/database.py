import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "monitoring.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Stations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT NOT NULL UNIQUE,
                min_value REAL NOT NULL,
                max_value REAL NOT NULL,
                enabled INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Readings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                station_id INTEGER NOT NULL,
                value REAL NOT NULL,
                raw_message TEXT,
                is_alert INTEGER DEFAULT 0,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (station_id) REFERENCES stations (id)
            )
        """)
        
        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reading_id INTEGER NOT NULL,
                acknowledged INTEGER DEFAULT 0,
                acknowledged_at TIMESTAMP,
                resolution_notes TEXT,
                resolved_by TEXT,
                FOREIGN KEY (reading_id) REFERENCES readings (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_station(self, name: str, phone_number: str, min_value: float, max_value: float) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stations (name, phone_number, min_value, max_value)
            VALUES (?, ?, ?, ?)
        """, (name, phone_number, min_value, max_value))
        station_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return station_id
    
    def update_station(self, station_id: int, name: str, phone_number: str, 
                      min_value: float, max_value: float, enabled: bool):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE stations 
            SET name=?, phone_number=?, min_value=?, max_value=?, enabled=?
            WHERE id=?
        """, (name, phone_number, min_value, max_value, 1 if enabled else 0, station_id))
        conn.commit()
        conn.close()
    
    def delete_station(self, station_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stations WHERE id=?", (station_id,))
        conn.commit()
        conn.close()
    
    def get_all_stations(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stations ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_station_by_phone(self, phone_number: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stations WHERE phone_number=?", (phone_number,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def add_reading(self, station_id: int, value: float, raw_message: str = "") -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if reading is out of range
        cursor.execute("SELECT min_value, max_value FROM stations WHERE id=?", (station_id,))
        station = cursor.fetchone()
        is_alert = 0
        if station:
            min_val, max_val = station
            is_alert = 1 if (value < min_val or value > max_val) else 0
        
        cursor.execute("""
            INSERT INTO readings (station_id, value, raw_message, is_alert)
            VALUES (?, ?, ?, ?)
        """, (station_id, value, raw_message, is_alert))
        reading_id = cursor.lastrowid
        
        # Create alert if needed
        if is_alert:
            cursor.execute("INSERT INTO alerts (reading_id) VALUES (?)", (reading_id,))
        
        conn.commit()
        conn.close()
        return reading_id
    
    def get_latest_readings(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id as station_id, s.name, s.phone_number, s.min_value, s.max_value,
                   r.value, r.is_alert, r.received_at, s.enabled
            FROM stations s
            LEFT JOIN readings r ON s.id = r.station_id
            WHERE r.id IN (
                SELECT MAX(id) FROM readings GROUP BY station_id
            ) OR r.id IS NULL
            ORDER BY s.name
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_station_history(self, station_id: int, limit: int = 100) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, a.resolution_notes, a.resolved_by, a.acknowledged_at
            FROM readings r
            LEFT JOIN alerts a ON r.id = a.reading_id
            WHERE r.station_id=? 
            ORDER BY r.received_at DESC 
            LIMIT ?
        """, (station_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_active_alerts(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id as alert_id, s.name, s.phone_number, r.value, 
                   s.min_value, s.max_value, r.received_at
            FROM alerts a
            JOIN readings r ON a.reading_id = r.id
            JOIN stations s ON r.station_id = s.id
            WHERE a.acknowledged = 0
            ORDER BY r.received_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def acknowledge_alert(self, alert_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE alerts 
            SET acknowledged=1, acknowledged_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (alert_id,))
        conn.commit()
        conn.close()
    
    def add_resolution_notes(self, reading_id: int, notes: str, resolved_by: str = ""):
        """Add resolution notes to a reading's alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find alert for this reading
        cursor.execute("SELECT id FROM alerts WHERE reading_id=?", (reading_id,))
        alert = cursor.fetchone()
        
        if alert:
            cursor.execute("""
                UPDATE alerts 
                SET resolution_notes=?, resolved_by=?, acknowledged=1, acknowledged_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (notes, resolved_by, alert[0]))
        
        conn.commit()
        conn.close()
    
    def get_reading_with_notes(self, reading_id: int) -> dict:
        """Get reading with resolution notes"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.*, a.resolution_notes, a.resolved_by, a.acknowledged_at
            FROM readings r
            LEFT JOIN alerts a ON r.id = a.reading_id
            WHERE r.id=?
        """, (reading_id,))
        
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
