"""
Todo Database Module
Author: Parvez Zamadar (@paruuvez)
Description: Database operations for Todo App
"""

import sqlite3
from datetime import datetime, date
from typing import List, Optional, Tuple
import threading

class TodoDatabase:
    """Thread-safe database operations for Todo App"""
    
    def __init__(self, db_name: str = "todo.db"):
        self.db_name = db_name
        self._local = threading.local()
        self.create_table()
    
    def get_connection(self):
        """Get thread-local database connection"""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(
                self.db_name, 
                check_same_thread=False
            )
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn
    
    def close_connection(self):
        """Close thread-local database connection"""
        if hasattr(self._local, 'conn') and self._local.conn:
            self._local.conn.close()
            self._local.conn = None
    
    def create_table(self):
        """Create tasks and categories tables"""
        conn = self.get_connection()
        
        # Create tasks table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                due_date TEXT,
                category TEXT DEFAULT 'general',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
        ''')
        
        # Create categories table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#3498db'
            )
        ''')
        
        # Insert default categories
        default_categories = [
            ('general', '#3498db'),
            ('work', '#2ecc71'),
            ('personal', '#9b59b6'),
            ('shopping', '#e74c3c'),
            ('health', '#1abc9c'),
            ('education', '#f39c12'),
            ('finance', '#27ae60'),
            ('travel', '#8e44ad')
        ]
        
        for name, color in default_categories:
            conn.execute('''
                INSERT OR IGNORE INTO categories (name, color) 
                VALUES (?, ?)
            ''', (name, color))
        
        conn.commit()
    
    def add_task(self, title: str, description: str = "", 
                 priority: str = "medium", due_date: str = None,
                 category: str = "general") -> int:
        """Add a new task to database"""
        conn = self.get_connection()
        cursor = conn.execute('''
            INSERT INTO tasks (title, description, priority, due_date, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, priority, due_date, category))
        conn.commit()
        return cursor.lastrowid
    
    def get_task(self, task_id: int) -> Optional[dict]:
        """Get a single task by ID"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_tasks(self, status: str = None, category: str = None, 
                      priority: str = None) -> List[dict]:
        """Get all tasks with optional filters"""
        conn = self.get_connection()
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
        query += " ORDER BY "
        query += "CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, "
        query += "CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, "
        query += "due_date ASC, created_at DESC"
        
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_today_tasks(self) -> List[dict]:
        """Get tasks due today"""
        conn = self.get_connection()
        today = date.today().strftime("%Y-%m-%d")
        cursor = conn.execute('''
            SELECT * FROM tasks 
            WHERE due_date = ? AND status = 'pending'
            ORDER BY priority DESC
        ''', (today,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_overdue_tasks(self) -> List[dict]:
        """Get overdue tasks"""
        conn = self.get_connection()
        today = date.today().strftime("%Y-%m-%d")
        cursor = conn.execute('''
            SELECT * FROM tasks 
            WHERE due_date < ? AND status = 'pending'
            ORDER BY due_date ASC
        ''', (today,))
        return [dict(row) for row in cursor.fetchall()]
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update task fields"""
        if not kwargs:
            return False
        
        conn = self.get_connection()
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE tasks SET {set_clause} WHERE id = ?"
        params = list(kwargs.values()) + [task_id]
        
        conn.execute(query, params)
        conn.commit()
        return True
    
    def complete_task(self, task_id: int) -> bool:
        """Mark task as completed"""
        conn = self.get_connection()
        completed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute('''
            UPDATE tasks 
            SET status = 'completed', completed_at = ?
            WHERE id = ?
        ''', (completed_time, task_id))
        conn.commit()
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        conn = self.get_connection()
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return True
    
    def search_tasks(self, search_term: str) -> List[dict]:
        """Search tasks by title or description"""
        conn = self.get_connection()
        search_pattern = f"%{search_term}%"
        cursor = conn.execute('''
            SELECT * FROM tasks 
            WHERE title LIKE ? OR description LIKE ? 
            ORDER BY priority DESC, due_date ASC
        ''', (search_pattern, search_pattern))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_task_statistics(self) -> dict:
        """Get task statistics"""
        conn = self.get_connection()
        
        # Get basic stats
        cursor = conn.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN due_date < date('now') AND status = 'pending' THEN 1 ELSE 0 END) as overdue
            FROM tasks
        ''')
        stats = cursor.fetchone()
        
        # Get today's tasks count
        cursor = conn.execute('''
            SELECT COUNT(*) as today_tasks 
            FROM tasks 
            WHERE due_date = date('now') AND status = 'pending'
        ''')
        today_stats = cursor.fetchone()
        
        # Get category distribution
        cursor = conn.execute('''
            SELECT category, COUNT(*) as count,
                   CASE 
                       WHEN status = 'completed' THEN 'completed'
                       ELSE 'pending'
                   END as task_status
            FROM tasks 
            GROUP BY category, task_status
        ''')
        categories = cursor.fetchall()
        
        return {
            'total': stats['total'] or 0,
            'completed': stats['completed'] or 0,
            'pending': stats['pending'] or 0,
            'overdue': stats['overdue'] or 0,
            'today': today_stats['today_tasks'] or 0,
            'categories': [dict(row) for row in categories]
        }
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT DISTINCT name FROM categories ORDER BY name")
        return ["all"] + [row['name'] for row in cursor.fetchall()]
    
    def add_category(self, name: str, color: str = "#3498db") -> bool:
        """Add a new category"""
        conn = self.get_connection()
        try:
            conn.execute('''
                INSERT INTO categories (name, color)
                VALUES (?, ?)
            ''', (name, color))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def export_to_csv(self, filepath: str) -> bool:
        """Export tasks to CSV file"""
        import csv
        try:
            conn = self.get_connection()
            cursor = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            tasks = cursor.fetchall()
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['ID', 'Title', 'Description', 'Status', 
                               'Priority', 'Due Date', 'Category', 
                               'Created At', 'Completed At'])
                # Write data
                for task in tasks:
                    writer.writerow(task)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False