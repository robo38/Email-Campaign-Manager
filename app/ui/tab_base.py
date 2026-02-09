"""
Tab base class for consistent structure
"""
from tkinter import ttk
import tkinter as tk


class TabBase:
    """Base class for all tabs"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent, style="Main.TFrame")
        self.create_widgets()
    
    def create_widgets(self):
        """Override in subclasses"""
        raise NotImplementedError("Subclasses must implement create_widgets()")
    
    def create_header(self, title, subtitle, accent_color="#6366f1"):
        """Create standard tab header"""
        header_frame = ttk.Frame(self.frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 0))
        
        # Accent line
        accent_line = tk.Frame(header_frame, bg=accent_color, height=3)
        accent_line.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        ttk.Label(header_frame, text=title, style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        
        # Subtitle
        ttk.Label(header_frame, text=subtitle, foreground="#94a3b8", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 20))
        
        return header_frame
