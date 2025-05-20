import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='data/nigedease.db'):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Create query logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS query_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_text TEXT NOT NULL,
                    response_text TEXT,
                    language TEXT CHECK(language IN ('en', 'am')),
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create demo data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS demo_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    data JSON NOT NULL
                )
            ''')
            conn.commit()

    def log_query(self, query_text, response_text, language):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO query_logs (query_text, response_text, language) VALUES (?, ?, ?)',
                (query_text, response_text, language)
            )
            conn.commit()

    def get_query_stats(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Get total queries
            cursor.execute('SELECT COUNT(*) FROM query_logs')
            total_queries = cursor.fetchone()[0]
            
            # Get language distribution
            cursor.execute('''
                SELECT language, COUNT(*) as count 
                FROM query_logs 
                GROUP BY language
            ''')
            language_stats = dict(cursor.fetchall())
            
            # Get most common queries
            cursor.execute('''
                SELECT query_text, COUNT(*) as count 
                FROM query_logs 
                GROUP BY query_text 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            common_queries = cursor.fetchall()
            
            return {
                'total_queries': total_queries,
                'language_stats': language_stats,
                'common_queries': common_queries
            }

    def init_demo_data(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Sample inventory data
            inventory_data = {
                "branches": {
                    "Addis Ababa": {
                        "notebooks": 150,
                        "pens": 300,
                        "calculators": 50
                    },
                    "Bahir Dar": {
                        "notebooks": 100,
                        "pens": 200,
                        "calculators": 30
                    }
                }
            }
            
            # Sample sales data
            sales_data = {
                "weekly_sales": {
                    "Addis Ababa": {
                        "notebooks": 45,
                        "pens": 120,
                        "calculators": 10
                    },
                    "Bahir Dar": {
                        "notebooks": 30,
                        "pens": 80,
                        "calculators": 5
                    }
                }
            }
            
            cursor.execute('INSERT OR REPLACE INTO demo_data (id, type, data) VALUES (1, "inventory", ?)',
                         (str(inventory_data),))
            cursor.execute('INSERT OR REPLACE INTO demo_data (id, type, data) VALUES (2, "sales", ?)',
                         (str(sales_data),))
            conn.commit()

    def get_demo_data(self, data_type):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT data FROM demo_data WHERE type = ?', (data_type,))
            result = cursor.fetchone()
            return eval(result[0]) if result else None 