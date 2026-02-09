"""
Main Application Entry Point
"""
import tkinter as tk
from tkinter import ttk
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ui.styles import AppStyles
from app.config import ConfigManager
from app.html_parser import HTMLTextExtractor
from app.email_sender import EmailSender


class BulkEmailSender:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("✉️ Professional Email Campaign Manager")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a1a")
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        self.temp_html_file = None
        self.embedded_images = {}
        self.is_connected = False
        self.connection_status_label = None
        self.email_sender = None
        
        # Setup styles
        AppStyles.configure_styles()
        
        # Create main container first
        main_container = ttk.Frame(root, style="Main.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar
        self.create_top_toolbar()
        
        # Create notebook
        self.notebook = ttk.Notebook(main_container, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Import and create tabs (lazy import to avoid circular dependencies)
        from app.ui.recipients_tab import RecipientsTab
        from app.ui.compose_tab import ComposeTab
        from app.ui.send_tab import SendTab
        
        self.recipients_tab = RecipientsTab(self.notebook, self)
        self.compose_tab = ComposeTab(self.notebook, self)
        self.send_tab = SendTab(self.notebook, self)
        
        self.notebook.add(self.recipients_tab.frame, text="  👥  Recipients  ")
        self.notebook.add(self.compose_tab.frame, text="  ✉️  Compose  ")
        self.notebook.add(self.send_tab.frame, text="  🚀  Send  ")
        
        # Start preview updates
        self.schedule_preview_update()
    
    def create_top_toolbar(self):
        """Create modern top toolbar with connection status"""
        toolbar = tk.Frame(self.root, bg="#13132b", height=65)
        toolbar.pack(fill=tk.X, side=tk.TOP, before=self.root.winfo_children()[0])
        
        # Separator line
        separator = tk.Frame(toolbar, bg="#252550", height=1)
        separator.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Left side - Connection button
        left_frame = tk.Frame(toolbar, bg="#13132b")
        left_frame.pack(side=tk.LEFT, padx=25, pady=12)
        
        # Connection indicator
        self.connection_indicator = tk.Canvas(left_frame, width=14, height=14, bg="#13132b", highlightthickness=0)
        self.connection_indicator.pack(side=tk.LEFT, padx=(0, 12))
        self.connection_circle = self.connection_indicator.create_oval(2, 2, 12, 12, fill=AppStyles.TEXT_MUTED, outline="")
        
        # Connection button
        self.connection_btn = tk.Button(
            left_frame,
            text="🔌 Connect SMTP",
            bg="#6366f1",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=24,
            pady=10,
            cursor="hand2",
            command=self.show_connection_dialog,
            activebackground="#4f46e5",
            activeforeground="white"
        )
        self.connection_btn.pack(side=tk.LEFT)
        
        # Hover effects
        self.connection_btn.bind("<Enter>", lambda e: self.connection_btn.config(bg="#4f46e5"))
        self.connection_btn.bind("<Leave>", lambda e: self.connection_btn.config(bg="#6366f1" if not self.is_connected else "#10b981"))
        
        # Status label
        self.connection_status_label = tk.Label(
            left_frame,
            text="Not Connected",
            bg="#13132b",
            fg="#94a3b8",
            font=("Segoe UI", 10)
        )
        self.connection_status_label.pack(side=tk.LEFT, padx=15)
        
        # Gear icon for SMTP settings
        self.settings_btn = tk.Button(
            left_frame,
            text="⚙️",
            bg="#13132b",
            fg="#f8fafc",
            font=("Segoe UI", 16),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.show_smtp_settings,
            activebackground="#252550",
            activeforeground="#f8fafc"
        )
        self.settings_btn.pack(side=tk.LEFT, padx=(10, 0))
        self.settings_btn.bind("<Enter>", lambda e: self.settings_btn.config(bg="#252550"))
        self.settings_btn.bind("<Leave>", lambda e: self.settings_btn.config(bg="#13132b"))
        
        # Right side - App info
        right_frame = tk.Frame(toolbar, bg="#13132b")
        right_frame.pack(side=tk.RIGHT, padx=25, pady=12)
        
        app_label = tk.Label(
            right_frame,
            text="📧 Professional Email Campaign Manager",
            bg="#13132b",
            fg="#f8fafc",
            font=("Segoe UI", 12, "bold")
        )
        app_label.pack()
        
        # Auto-connect if credentials saved
        if self.config_manager.get("server") and self.config_manager.get("email") and self.config_manager.get("password"):
            self.test_and_connect_auto()
    
    def show_connection_dialog(self):
        """Show connection dialog"""
        from app.ui.connection_dialog import ConnectionDialog
        ConnectionDialog(self.root, self)
    
    def show_smtp_settings(self):
        """Show SMTP settings dialog"""
        from app.ui.smtp_dialog import SMTPSettingsDialog
        SMTPSettingsDialog(self.root, self)
    
    def test_and_connect_auto(self):
        """Test connection automatically"""
        try:
            self.email_sender = EmailSender(
                self.config_manager.get("server"),
                self.config_manager.get("port"),
                self.config_manager.get("email"),
                self.config_manager.get("password"),
                self.config_manager.get("reply_to")
            )
            self.email_sender.test_connection()
            self.is_connected = True
            self.update_connection_status(True)
        except:
            self.email_sender = None
            self.is_connected = False
            self.update_connection_status(False)
    
    def update_connection_status(self, connected):
        """Update connection status indicator"""
        if connected:
            self.connection_indicator.itemconfig(self.connection_circle, fill="#10b981")
            self.connection_status_label.config(text="✓ Connected", fg="#10b981", font=("Segoe UI", 10, "bold"))
            self.connection_btn.config(text="✅ Connected", bg="#10b981")
            self.connection_btn.bind("<Leave>", lambda e: self.connection_btn.config(bg="#10b981"))
        else:
            self.connection_indicator.itemconfig(self.connection_circle, fill="#94a3b8")
            self.connection_status_label.config(text="Not Connected", fg="#94a3b8", font=("Segoe UI", 10))
            self.connection_btn.config(text="🔌 Connect SMTP", bg="#6366f1")
            self.connection_btn.bind("<Leave>", lambda e: self.connection_btn.config(bg="#6366f1"))
    
    def schedule_preview_update(self):
        """Schedule periodic preview updates"""
        if hasattr(self, 'compose_tab'):
            self.compose_tab.update_preview()
        self.root.after(1000, self.schedule_preview_update)
