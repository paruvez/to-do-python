"""
Todo GUI Application
Author: Parvez Zamadar (@paruuvez)
Description: Modern GUI Todo App with SQLite backend
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font, filedialog
from datetime import datetime, date
import sqlite3
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw
import os
import webbrowser

# Import TodoDatabase from the database module
try:
    from todo_database import TodoDatabase
except ImportError:
    # Fallback definition if import fails
    class TodoDatabase:
        def __init__(self, db_name: str = "todo.db"):
            pass
        def get_all_tasks(self, status=None, category=None, priority=None):
            return []
        def get_task(self, task_id):
            return None
        def add_task(self, title, description="", priority="medium", due_date=None, category="general"):
            return 1
        def update_task(self, task_id, **kwargs):
            return True
        def complete_task(self, task_id):
            return True
        def delete_task(self, task_id):
            return True
        def get_task_statistics(self):
            return {'total': 0, 'completed': 0, 'pending': 0, 'overdue': 0, 'today': 0, 'categories': []}
        def get_categories(self):
            return ["all", "general", "work", "personal", "shopping", "health", "education"]
        def add_category(self, name, color="#3498db"):
            return True
        def export_to_csv(self, filepath):
            return True
        def get_today_tasks(self):
            return []
        def get_overdue_tasks(self):
            return []


class TodoApp:
    """Main Todo Application Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("✅ TodoMaster Pro - Stay Organized")
        self.root.geometry("1300x750")
        self.root.configure(bg="#f5f7fa")
        
        # Center window on screen
        self.center_window()
        
        # Set window icon
        self.set_window_icon()
        
        # Initialize database
        self.db = TodoDatabase("todo_app.db")
        
        # Create modern fonts
        self.create_fonts()
        
        # Configure colors and styles
        self.setup_styles()
        
        # Application variables
        self.current_filter = "all"
        self.current_category = "all"
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        
        # Store images
        self.images = {}
        
        # Create UI
        self.create_ui()
        
        # Load initial data
        self.load_initial_data()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def set_window_icon(self):
        """Set window icon"""
        icon_paths = [
            'assets/icon.ico',
            'assets/logo.ico',
            'todo_icon.ico'
        ]
        
        for path in icon_paths:
            if os.path.exists(path):
                try:
                    self.root.iconbitmap(path)
                    break
                except:
                    continue
    
    def create_fonts(self):
        """Create custom fonts for modern look"""
        self.title_font = font.Font(
            family="Segoe UI", 
            size=18, 
            weight="bold"
        )
        self.header_font = font.Font(
            family="Segoe UI", 
            size=12, 
            weight="bold"
        )
        self.normal_font = font.Font(
            family="Segoe UI", 
            size=10
        )
        self.small_font = font.Font(
            family="Segoe UI", 
            size=9
        )
        self.big_font = font.Font(
            family="Segoe UI", 
            size=28, 
            weight="bold"
        )
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color palette
        self.colors = {
            'primary': '#4361ee',
            'secondary': '#3a0ca3',
            'success': '#4cc9f0',
            'danger': '#f72585',
            'warning': '#f8961e',
            'info': '#7209b7',
            'light': '#f8f9fa',
            'dark': '#212529',
            'bg': '#f5f7fa',
            'card': '#ffffff',
            'border': '#dee2e6'
        }
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=self.normal_font)
        style.map('Primary.TButton',
                 background=[('active', '#3a56d4')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white')
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white')
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white')
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['card'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Light.TFrame',
                       background=self.colors['bg'])
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.colors['card'],
                       font=self.title_font,
                       foreground=self.colors['dark'])
        
        style.configure('Header.TLabel',
                       background=self.colors['card'],
                       font=self.header_font,
                       foreground=self.colors['dark'])
    
    def create_ui(self):
        """Create the main user interface"""
        # Create header
        self.create_header()
        
        # Create main container
        main_container = ttk.Frame(self.root, style='Light.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Create sidebar and content area
        self.create_sidebar(main_container)
        self.create_content_area(main_container)
        
        # Create status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create application header with logo"""
        header = ttk.Frame(self.root, style='Card.TFrame')
        header.pack(fill=tk.X, padx=15, pady=15)
        
        # Logo and title container
        logo_container = ttk.Frame(header, style='Card.TFrame')
        logo_container.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Create logo
        self.create_logo(logo_container)
        
        # App title
        title_frame = ttk.Frame(logo_container, style='Card.TFrame')
        title_frame.pack(side=tk.LEFT, padx=(15, 0))
        
        title_label = ttk.Label(
            title_frame,
            text="TodoMaster Pro",
            style='Title.TLabel'
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Stay organized and boost productivity",
            font=self.small_font,
            foreground='#6c757d',
            background=self.colors['card']
        )
        subtitle_label.pack(anchor=tk.W)
        
        # Quick stats in header
        stats_frame = ttk.Frame(header, style='Card.TFrame')
        stats_frame.pack(side=tk.RIGHT, padx=20)
        
        self.header_stats = {
            'total': ttk.Label(stats_frame, text="0", font=self.big_font,
                              foreground=self.colors['primary'],
                              background=self.colors['card']),
            'pending': ttk.Label(stats_frame, text="0", font=self.big_font,
                                foreground=self.colors['warning'],
                                background=self.colors['card']),
            'completed': ttk.Label(stats_frame, text="0", font=self.big_font,
                                  foreground=self.colors['success'],
                                  background=self.colors['card'])
        }
        
        for i, (key, label) in enumerate(self.header_stats.items()):
            label.grid(row=0, column=i, padx=15)
            stat_name = ttk.Label(stats_frame, text=key.title(),
                                 font=self.small_font,
                                 foreground='#6c757d',
                                 background=self.colors['card'])
            stat_name.grid(row=1, column=i, padx=15)
    
    def create_logo(self, parent):
        """Create application logo"""
        try:
            # Try to load logo from file
            logo_paths = ['assets/logo.png', 'logo.png']
            logo_img = None
            
            for path in logo_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    img = img.resize((50, 50), Image.Resampling.LANCZOS)
                    logo_img = ImageTk.PhotoImage(img)
                    self.images['logo'] = logo_img
                    break
            
            if logo_img:
                logo_label = ttk.Label(parent, image=logo_img,
                                      background=self.colors['card'])
            else:
                # Create a simple logo
                img = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
                draw = ImageDraw.Draw(img)
                # Draw checkmark in circle
                draw.ellipse([5, 5, 45, 45], outline=self.colors['primary'], width=3)
                draw.line([(15, 25), (25, 35), (35, 20)], 
                         fill=self.colors['primary'], width=4)
                logo_img = ImageTk.PhotoImage(img)
                self.images['logo'] = logo_img
                logo_label = ttk.Label(parent, image=logo_img,
                                      background=self.colors['card'])
            
            logo_label.pack(side=tk.LEFT)
            
        except Exception as e:
            print(f"Logo error: {e}")
            # Fallback to text logo
            logo_label = ttk.Label(parent, text="✅",
                                  font=("Arial", 24),
                                  background=self.colors['card'])
            logo_label.pack(side=tk.LEFT)
    
    def create_sidebar(self, parent):
        """Create sidebar with filters and categories"""
        sidebar = ttk.Frame(parent, width=250, style='Card.TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Search box
        search_frame = ttk.Frame(sidebar, style='Card.TFrame')
        search_frame.pack(fill=tk.X, padx=15, pady=15)
        
        search_icon = ttk.Label(search_frame, text="🔍",
                               font=("Arial", 12),
                               background=self.colors['card'])
        search_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_entry = ttk.Entry(search_frame,
                                     textvariable=self.search_var,
                                     font=self.normal_font)
        self.search_entry.pack(fill=tk.X, expand=True)
        self.search_entry.insert(0, "Search tasks...")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
        
        # Filters section
        filters_frame = ttk.LabelFrame(sidebar, text=" Quick Filters ",
                                      style='Card.TFrame',
                                      padding=15)
        filters_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        filters = [
            ("📋 All Tasks", "all", self.colors['primary']),
            ("⏳ Pending", "pending", self.colors['warning']),
            ("✅ Completed", "completed", self.colors['success']),
            ("⚠️ Overdue", "overdue", self.colors['danger']),
            ("📅 Today", "today", self.colors['info'])
        ]
        
        for text, value, color in filters:
            btn = self.create_filter_button(filters_frame, text, value, color)
            btn.pack(fill=tk.X, pady=3)
        
        # Categories section
        categories_frame = ttk.LabelFrame(sidebar, text=" Categories ",
                                         style='Card.TFrame',
                                         padding=15)
        categories_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Category list with scrollbar
        cat_container = ttk.Frame(categories_frame, style='Card.TFrame')
        cat_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for scrollable categories
        self.cat_canvas = tk.Canvas(cat_container, bg=self.colors['card'],
                                   highlightthickness=0)
        cat_scrollbar = ttk.Scrollbar(cat_container, orient="vertical",
                                     command=self.cat_canvas.yview)
        self.cat_scroll_frame = ttk.Frame(self.cat_canvas, style='Card.TFrame')
        
        self.cat_scroll_frame.bind(
            "<Configure>",
            lambda e: self.cat_canvas.configure(scrollregion=self.cat_canvas.bbox("all"))
        )
        
        self.cat_canvas.create_window((0, 0), window=self.cat_scroll_frame, anchor="nw")
        self.cat_canvas.configure(yscrollcommand=cat_scrollbar.set)
        
        self.cat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add category button
        add_cat_btn = ttk.Button(sidebar, text="➕ Add Category",
                                command=self.add_category_dialog,
                                style='Primary.TButton')
        add_cat_btn.pack(fill=tk.X, padx=15, pady=(0, 15))
    
    def create_filter_button(self, parent, text, value, color):
        """Create a styled filter button"""
        btn = tk.Button(parent, text=text,
                       font=self.normal_font,
                       bg=self.colors['card'],
                       fg=color,
                       activebackground=color,
                       activeforeground='white',
                       bd=0,
                       padx=15,
                       pady=8,
                       cursor='hand2',
                       command=lambda v=value: self.filter_tasks(v))
        
        # Add hover effect
        def on_enter(e):
            btn['bg'] = '#f8f9fa'
        
        def on_leave(e):
            btn['bg'] = self.colors['card']
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_content_area(self, parent):
        """Create main content area"""
        content = ttk.Frame(parent, style='Card.TFrame')
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Toolbar
        self.create_toolbar(content)
        
        # Task list
        self.create_task_list(content)
        
        # Statistics panel
        self.create_statistics_panel(content)
    
    def create_toolbar(self, parent):
        """Create toolbar with action buttons"""
        toolbar = ttk.Frame(parent, style='Card.TFrame')
        toolbar.pack(fill=tk.X, padx=20, pady=20)
        
        # Left side buttons
        left_toolbar = ttk.Frame(toolbar, style='Card.TFrame')
        left_toolbar.pack(side=tk.LEFT)
        
        actions = [
            ("➕ Add Task", self.add_task_dialog, 'primary'),
            ("📊 Export", self.export_tasks, 'success'),
            ("🔄 Refresh", self.refresh_all, 'warning')
        ]
        
        for text, command, style_type in actions:
            if style_type == 'primary':
                btn_style = 'Primary.TButton'
            elif style_type == 'success':
                btn_style = 'Success.TButton'
            else:
                btn_style = 'Warning.TButton'
            
            btn = ttk.Button(left_toolbar, text=text,
                           command=command, style=btn_style)
            btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Right side buttons
        right_toolbar = ttk.Frame(toolbar, style='Card.TFrame')
        right_toolbar.pack(side=tk.RIGHT)
        
        # Task actions (enabled when task is selected)
        self.complete_btn = ttk.Button(right_toolbar, text="✅ Complete",
                                      command=self.complete_selected,
                                      state='disabled',
                                      style='Success.TButton')
        self.complete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.edit_btn = ttk.Button(right_toolbar, text="✏️ Edit",
                                  command=self.edit_selected,
                                  state='disabled')
        self.edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_btn = ttk.Button(right_toolbar, text="🗑️ Delete",
                                    command=self.delete_selected,
                                    state='disabled',
                                    style='Danger.TButton')
        self.delete_btn.pack(side=tk.LEFT)
    
    def create_task_list(self, parent):
        """Create task list with Treeview"""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create Treeview with custom styling
        self.tree = ttk.Treeview(list_frame,
                                columns=("ID", "Title", "Priority", "Due", 
                                        "Status", "Category", "Created"),
                                show="headings",
                                height=15)
        
        # Define columns
        columns = [
            ("ID", 50, 'center'),
            ("Title", 300, 'w'),
            ("Priority", 100, 'center'),
            ("Due", 120, 'center'),
            ("Status", 100, 'center'),
            ("Category", 120, 'center'),
            ("Created", 150, 'center')
        ]
        
        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        # Configure tags for styling
        self.tree.tag_configure('high', background='#ffebee')
        self.tree.tag_configure('medium', background='#fff8e1')
        self.tree.tag_configure('low', background='#e8f5e9')
        self.tree.tag_configure('completed', foreground='#9e9e9e')
        self.tree.tag_configure('overdue', foreground='#d32f2f', font=('Segoe UI', 9, 'bold'))
        
        # Add scrollbars
        v_scroll = ttk.Scrollbar(list_frame, orient="vertical",
                                command=self.tree.yview)
        h_scroll = ttk.Scrollbar(list_frame, orient="horizontal",
                                command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set,
                           xscrollcommand=h_scroll.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_task_select)
        self.tree.bind('<Double-Button-1>', self.on_task_double_click)
    
    def create_statistics_panel(self, parent):
        """Create statistics panel"""
        stats_frame = ttk.LabelFrame(parent, text=" Statistics Dashboard ",
                                    style='Card.TFrame',
                                    padding=20)
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Create stats grid
        stats_grid = ttk.Frame(stats_frame, style='Card.TFrame')
        stats_grid.pack(fill=tk.X)
        
        stats_data = [
            ("📋 Total", "total", self.colors['primary']),
            ("✅ Completed", "completed", self.colors['success']),
            ("⏳ Pending", "pending", self.colors['warning']),
            ("⚠️ Overdue", "overdue", self.colors['danger']),
            ("📅 Today", "today", self.colors['info']),
            ("⚡ Productivity", "productivity", "#9c27b0")
        ]
        
        self.stats_labels = {}
        
        for i, (label, key, color) in enumerate(stats_data):
            frame = ttk.Frame(stats_grid, style='Card.TFrame')
            frame.grid(row=i//3, column=i%3, sticky="nsew", padx=10, pady=10)
            stats_grid.columnconfigure(i%3, weight=1)
            
            # Icon and label
            icon_label = ttk.Label(frame, text=label.split()[0],
                                  font=("Arial", 14),
                                  background=self.colors['card'])
            icon_label.pack(anchor=tk.W)
            
            name_label = ttk.Label(frame, text=label.split()[1],
                                  font=self.small_font,
                                  foreground='#6c757d',
                                  background=self.colors['card'])
            name_label.pack(anchor=tk.W)
            
            # Value
            self.stats_labels[key] = ttk.Label(frame, text="0",
                                              font=font.Font(size=24, weight="bold"),
                                              foreground=color,
                                              background=self.colors['card'])
            self.stats_labels[key].pack(anchor=tk.W, pady=(5, 0))
        
        # Progress bar
        progress_frame = ttk.Frame(stats_frame, style='Card.TFrame')
        progress_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Label(progress_frame, text="Completion Progress",
                 font=self.header_font,
                 background=self.colors['card']).pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                          length=100,
                                          mode='determinate',
                                          style='Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="0%",
                                       font=self.normal_font,
                                       background=self.colors['card'])
        self.progress_label.pack(anchor=tk.E)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_bar = ttk.Frame(self.root, style='Card.TFrame')
        status_bar.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Left side - App info
        left_status = ttk.Frame(status_bar, style='Card.TFrame')
        left_status.pack(side=tk.LEFT, padx=10)
        
        app_info = ttk.Label(left_status,
                            text="TodoMaster Pro v1.0 | Developed by Parvez Zamadar (@paruuvez)",
                            font=self.small_font,
                            foreground='#6c757d',
                            background=self.colors['card'])
        app_info.pack(side=tk.LEFT)
        
        # Right side - Task count and time
        right_status = ttk.Frame(status_bar, style='Card.TFrame')
        right_status.pack(side=tk.RIGHT, padx=10)
        
        self.status_label = ttk.Label(right_status,
                                     text="Ready",
                                     font=self.small_font,
                                     foreground='#6c757d',
                                     background=self.colors['card'])
        self.status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Current time
        self.time_label = ttk.Label(right_status,
                                   font=self.small_font,
                                   foreground='#6c757d',
                                   background=self.colors['card'])
        self.time_label.pack(side=tk.LEFT)
        self.update_time()
    
    def load_initial_data(self):
        """Load initial data into UI"""
        self.refresh_category_list()
        self.refresh_task_list()
        self.update_statistics()
        self.update_header_stats()
    
    def refresh_category_list(self):
        """Refresh category list in sidebar"""
        # Clear existing widgets
        for widget in self.cat_scroll_frame.winfo_children():
            widget.destroy()
        
        # Add "All Categories" option
        all_btn = self.create_category_button("All Categories", "all", "#6c757d")
        all_btn.pack(fill=tk.X, pady=2)
        
        # Add actual categories
        categories = self.db.get_categories()[1:]  # Skip "all"
        for category in categories:
            # Get category color from database
            color = "#3498db"  # Default color
            btn = self.create_category_button(category, category, color)
            btn.pack(fill=tk.X, pady=2)
    
    def create_category_button(self, text, value, color):
        """Create a category button with colored dot"""
        btn_frame = ttk.Frame(self.cat_scroll_frame, style='Card.TFrame')
        
        # Colored dot
        dot_canvas = tk.Canvas(btn_frame, width=10, height=10,
                              bg=self.colors['card'], highlightthickness=0)
        dot_canvas.create_oval(2, 2, 8, 8, fill=color, outline="")
        dot_canvas.pack(side=tk.LEFT, padx=(10, 5))
        
        # Button
        btn = tk.Button(btn_frame, text=text,
                       font=self.small_font,
                       bg=self.colors['card'],
                       fg=self.colors['dark'],
                       activebackground='#f8f9fa',
                       activeforeground=self.colors['dark'],
                       bd=0,
                       anchor='w',
                       padx=5,
                       pady=8,
                       cursor='hand2',
                       command=lambda v=value: self.filter_by_category(v))
        btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Hover effects
        def on_enter(e):
            btn['bg'] = '#f8f9fa'
            dot_canvas['bg'] = '#f8f9fa'
        
        def on_leave(e):
            btn['bg'] = self.colors['card']
            dot_canvas['bg'] = self.colors['card']
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        dot_canvas.bind("<Enter>", on_enter)
        dot_canvas.bind("<Leave>", on_leave)
        
        return btn_frame
    
    def refresh_task_list(self):
        """Refresh task list in Treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get tasks based on current filter
        if self.current_filter == 'all':
            tasks = self.db.get_all_tasks()
        elif self.current_filter == 'pending':
            tasks = self.db.get_all_tasks(status='pending')
        elif self.current_filter == 'completed':
            tasks = self.db.get_all_tasks(status='completed')
        elif self.current_filter == 'overdue':
            tasks = self.db.get_overdue_tasks()
        elif self.current_filter == 'today':
            tasks = self.db.get_today_tasks()
        else:
            tasks = self.db.get_all_tasks()
        
        # Apply category filter
        if self.current_category != 'all':
            tasks = [t for t in tasks if t['category'] == self.current_category]
        
        # Apply search filter
        search_text = self.search_var.get().lower()
        if search_text and search_text != "search tasks...":
            tasks = [t for t in tasks 
                    if search_text in t['title'].lower() 
                    or search_text in (t['description'] or '').lower()]
        
        # Add tasks to tree
        for task in tasks:
            # Determine tags for styling
            tags = [task['priority']]
            if task['status'] == 'completed':
                tags.append('completed')
            
            # Check if overdue
            if task['due_date'] and task['status'] == 'pending':
                try:
                    due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                    if due_date < date.today():
                        tags.append('overdue')
                except:
                    pass
            
            # Format dates
            due_date = task['due_date'] or "No due date"
            created_date = datetime.strptime(task['created_at'], 
                                           "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")
            
            # Insert into tree
            self.tree.insert('', 'end',
                            values=(task['id'],
                                   task['title'],
                                   task['priority'].title(),
                                   due_date,
                                   task['status'].title(),
                                   task['category'].title(),
                                   created_date),
                            tags=tuple(tags))
    
    def update_statistics(self):
        """Update statistics display"""
        stats = self.db.get_task_statistics()
        
        # Update numeric stats
        for key in ['total', 'completed', 'pending', 'overdue', 'today']:
            if key in self.stats_labels:
                self.stats_labels[key].config(text=str(stats[key]))
        
        # Calculate and update productivity
        if stats['total'] > 0:
            productivity = (stats['completed'] / stats['total']) * 100
            self.stats_labels['productivity'].config(text=f"{productivity:.0f}%")
        else:
            self.stats_labels['productivity'].config(text="0%")
        
        # Update progress bar
        if stats['total'] > 0:
            completion_rate = (stats['completed'] / stats['total']) * 100
            self.progress_bar['value'] = completion_rate
            self.progress_label.config(text=f"{completion_rate:.1f}%")
        else:
            self.progress_bar['value'] = 0
            self.progress_label.config(text="0%")
    
    def update_header_stats(self):
        """Update header statistics"""
        stats = self.db.get_task_statistics()
        self.header_stats['total'].config(text=str(stats['total']))
        self.header_stats['pending'].config(text=str(stats['pending']))
        self.header_stats['completed'].config(text=str(stats['completed']))
    
    def update_time(self):
        """Update current time in status bar"""
        current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        self.time_label.config(text=current_time)
        self.root.after(60000, self.update_time)  # Update every minute
    
    def on_search_focus_in(self, event):
        """Handle search field focus in"""
        if self.search_entry.get() == "Search tasks...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground='black')
    
    def on_search_focus_out(self, event):
        """Handle search field focus out"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search tasks...")
            self.search_entry.config(foreground='gray')
    
    def on_search_changed(self, *args):
        """Handle search text changes"""
        self.refresh_task_list()
    
    def filter_tasks(self, filter_type):
        """Filter tasks by type"""
        self.current_filter = filter_type
        self.refresh_task_list()
        self.update_status(f"Filtered by: {filter_type.title()}")
    
    def filter_by_category(self, category):
        """Filter tasks by category"""
        self.current_category = category
        self.refresh_task_list()
        if category == 'all':
            self.update_status("Showing all categories")
        else:
            self.update_status(f"Filtered by category: {category}")
    
    def on_task_select(self, event):
        """Handle task selection"""
        selection = self.tree.selection()
        if selection:
            # Enable action buttons
            self.complete_btn.config(state='normal')
            self.edit_btn.config(state='normal')
            self.delete_btn.config(state='normal')
            
            # Show task details in status
            task_id = self.tree.item(selection[0])['values'][0]
            self.update_status(f"Selected task ID: {task_id}")
        else:
            # Disable action buttons
            self.complete_btn.config(state='disabled')
            self.edit_btn.config(state='disabled')
            self.delete_btn.config(state='disabled')
    
    def on_task_double_click(self, event):
        """Handle task double click"""
        self.edit_selected()
    
    def add_task_dialog(self):
        """Open add task dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Add New Task")
        dialog.geometry("500x600")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Create form
        self.create_task_form(dialog, None, "Add Task")
    
    def edit_selected(self):
        """Edit selected task"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a task to edit.")
            return
        
        task_id = self.tree.item(selection[0])['values'][0]
        task = self.db.get_task(task_id)
        
        if not task:
            messagebox.showerror("Error", "Task not found!")
            return
        
        # Open edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("✏️ Edit Task")
        dialog.geometry("500x600")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Create form
        self.create_task_form(dialog, task, "Edit Task")
    
    def create_task_form(self, parent, task, title):
        """Create task form for add/edit"""
        form_frame = ttk.Frame(parent, style='Card.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(form_frame, text=title,
                 font=self.title_font,
                 background=self.colors['card']).pack(anchor=tk.W, pady=(0, 20))
        
        # Title field
        ttk.Label(form_frame, text="Task Title *",
                 font=self.header_font,
                 background=self.colors['card']).pack(anchor=tk.W)
        title_var = tk.StringVar(value=task['title'] if task else "")
        title_entry = ttk.Entry(form_frame, textvariable=title_var,
                               font=self.normal_font)
        title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Description field
        ttk.Label(form_frame, text="Description",
                 font=self.header_font,
                 background=self.colors['card']).pack(anchor=tk.W)
        desc_text = scrolledtext.ScrolledText(form_frame, height=6,
                                             font=self.normal_font)
        desc_text.pack(fill=tk.X, pady=(0, 15))
        if task and task['description']:
            desc_text.insert("1.0", task['description'])
        
        # Priority, Due Date, Category in grid
        grid_frame = ttk.Frame(form_frame, style='Card.TFrame')
        grid_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Priority
        ttk.Label(grid_frame, text="Priority",
                 font=self.header_font,
                 background=self.colors['card']).grid(row=0, column=0, sticky=tk.W, pady=5)
        priority_var = tk.StringVar(value=task['priority'] if task else "medium")
        priority_combo = ttk.Combobox(grid_frame, textvariable=priority_var,
                                     values=["high", "medium", "low"],
                                     state='readonly', width=15)
        priority_combo.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # Due Date
        ttk.Label(grid_frame, text="Due Date",
                 font=self.header_font,
                 background=self.colors['card']).grid(row=0, column=1, sticky=tk.W, pady=5, padx=20)
        due_date_entry = DateEntry(grid_frame, width=15,
                                  background='darkblue',
                                  foreground='white',
                                  borderwidth=2,
                                  date_pattern='yyyy-mm-dd')
        due_date_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 10), padx=20)
        if task and task['due_date']:
            due_date_entry.set_date(datetime.strptime(task['due_date'], "%Y-%m-%d"))
        
        # Category
        ttk.Label(grid_frame, text="Category",
                 font=self.header_font,
                 background=self.colors['card']).grid(row=0, column=2, sticky=tk.W, pady=5)
        category_var = tk.StringVar(value=task['category'] if task else "general")
        category_combo = ttk.Combobox(grid_frame, textvariable=category_var,
                                     values=self.db.get_categories()[1:],
                                     state='readonly', width=15)
        category_combo.grid(row=1, column=2, sticky=tk.W, pady=(0, 10))
        
        # Status (only for edit)
        if task:
            ttk.Label(grid_frame, text="Status",
                     font=self.header_font,
                     background=self.colors['card']).grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
            status_var = tk.StringVar(value=task['status'])
            status_combo = ttk.Combobox(grid_frame, textvariable=status_var,
                                       values=["pending", "completed"],
                                       state='readonly', width=15)
            status_combo.grid(row=3, column=0, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(form_frame, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=20)
        
        def save_task():
            if not title_var.get().strip():
                messagebox.showerror("Error", "Task title is required!")
                return
            
            task_data = {
                'title': title_var.get().strip(),
                'description': desc_text.get("1.0", tk.END).strip(),
                'priority': priority_var.get(),
                'due_date': due_date_entry.get_date().strftime("%Y-%m-%d"),
                'category': category_var.get()
            }
            
            if task:
                # Update existing task
                if 'status_var' in locals():
                    task_data['status'] = status_var.get()
                    if status_var.get() == 'completed' and task['status'] != 'completed':
                        task_data['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.db.update_task(task['id'], **task_data)
                messagebox.showinfo("Success", "Task updated successfully!")
            else:
                # Add new task
                self.db.add_task(**task_data)
                messagebox.showinfo("Success", "Task added successfully!")
            
            parent.destroy()  # Fixed: Use parent instead of undefined dialog variable
            self.refresh_all()
        
        def cancel():
            parent.destroy()  # Fixed: Use parent instead of undefined dialog variable
        
        ttk.Button(button_frame, text="💾 Save",
                  command=save_task,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Cancel",
                  command=cancel).pack(side=tk.LEFT)
    
    def complete_selected(self):
        """Complete selected task"""
        selection = self.tree.selection()
        if not selection:
            return
        
        task_id = self.tree.item(selection[0])['values'][0]
        self.db.complete_task(task_id)
        self.refresh_all()
        self.update_status(f"Task {task_id} marked as completed")
    
    def delete_selected(self):
        """Delete selected task"""
        selection = self.tree.selection()
        if not selection:
            return
        
        task_id = self.tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete",
                              f"Are you sure you want to delete task #{task_id}?",
                              icon='warning'):
            self.db.delete_task(task_id)
            self.refresh_all()
            self.update_status(f"Task {task_id} deleted")
    
    def add_category_dialog(self):
        """Open add category dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Category")
        dialog.geometry("300x200")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        form_frame = ttk.Frame(dialog, style='Card.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Add New Category",
                 font=self.title_font,
                 background=self.colors['card']).pack(anchor=tk.W, pady=(0, 20))
        
        # Category name
        ttk.Label(form_frame, text="Category Name",
                 font=self.header_font,
                 background=self.colors['card']).pack(anchor=tk.W)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=name_var,
                              font=self.normal_font)
        name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Color selection
        ttk.Label(form_frame, text="Color",
                 font=self.header_font,
                 background=self.colors['card']).pack(anchor=tk.W)
        color_var = tk.StringVar(value="#3498db")
        color_combo = ttk.Combobox(form_frame, textvariable=color_var,
                                  values=["#3498db", "#2ecc71", "#9b59b6",
                                          "#e74c3c", "#1abc9c", "#f39c12",
                                          "#27ae60", "#8e44ad"],
                                  state='readonly')
        color_combo.pack(fill=tk.X, pady=(0, 20))
        
        def save_category():
            if not name_var.get().strip():
                messagebox.showerror("Error", "Category name is required!")
                return
            
            if self.db.add_category(name_var.get().strip(), color_var.get()):
                messagebox.showinfo("Success", "Category added successfully!")
                dialog.destroy()
                self.refresh_category_list()
            else:
                messagebox.showerror("Error", "Category already exists!")
        
        def cancel():
            dialog.destroy()
        
        button_frame = ttk.Frame(form_frame, style='Card.TFrame')
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add",
                  command=save_category,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Cancel",
                  command=cancel).pack(side=tk.LEFT)
    
    def export_tasks(self):
        """Export tasks to CSV file"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"todo_export_{date.today()}.csv"
        )
        
        if filepath:
            if self.db.export_to_csv(filepath):
                messagebox.showinfo("Success", f"Tasks exported to:\n{filepath}")
                self.update_status(f"Tasks exported to {os.path.basename(filepath)}")
            else:
                messagebox.showerror("Error", "Failed to export tasks")
    
    def refresh_all(self):
        """Refresh all UI components"""
        self.refresh_task_list()
        self.update_statistics()
        self.update_header_stats()
        self.update_status("Refreshed")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
    
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<F5>', lambda e: self.refresh_all())
        self.root.bind('<Control-n>', lambda e: self.add_task_dialog())
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        self.root.bind('<Control-s>', lambda e: self.export_tasks())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus())
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    # Check and install required packages
    try:
        from tkcalendar import DateEntry
        from PIL import Image, ImageTk, ImageDraw
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please run: pip install tkcalendar Pillow")
        return
    
    # Create and run application
    root = tk.Tk()
    app = TodoApp(root)
    app.run()


if __name__ == "__main__":
    main()