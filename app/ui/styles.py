"""
UI Styling Configuration
"""
from tkinter import ttk


class AppStyles:
    """Application styling configuration"""
    
    # Ultra-modern color palette
    BG_DARK = "#0a0a1a"
    BG_CARD = "#13132b"
    BG_ELEVATED = "#1a1a3a"
    BG_HOVER = "#252550"
    
    ACCENT_PRIMARY = "#6366f1"
    ACCENT_SECONDARY = "#06b6d4"
    ACCENT_SUCCESS = "#10b981"
    ACCENT_WARNING = "#f59e0b"
    ACCENT_ERROR = "#ef4444"
    
    TEXT_PRIMARY = "#f8fafc"
    TEXT_SECONDARY = "#cbd5e1"
    TEXT_MUTED = "#94a3b8"
    
    @staticmethod
    def configure_styles():
        """Configure TTK styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        style.configure("Main.TFrame", background=AppStyles.BG_DARK)
        
        # Notebook (Tabs)
        style.configure("TNotebook", 
                       background=AppStyles.BG_DARK, 
                       borderwidth=0,
                       tabmargins=[0, 5, 0, 0])
        
        style.configure("TNotebook.Tab",
                       background=AppStyles.BG_CARD,
                       foreground=AppStyles.TEXT_MUTED,
                       padding=[28, 14],
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0)
        
        style.map("TNotebook.Tab",
                 background=[("selected", AppStyles.BG_ELEVATED)],
                 foreground=[("selected", AppStyles.TEXT_PRIMARY)],
                 padding=[("selected", [28, 14])],
                 relief=[("selected", "flat")])

        # Card frames
        style.configure("Card.TFrame", 
                       background=AppStyles.BG_CARD, 
                       relief="flat",
                       borderwidth=0)

        # Labels
        style.configure("TLabel",
                       background=AppStyles.BG_CARD,
                       foreground=AppStyles.TEXT_PRIMARY,
                       font=("Segoe UI", 10))
        
        style.configure("Header.TLabel",
                       background=AppStyles.BG_CARD,
                       foreground=AppStyles.TEXT_PRIMARY,
                       font=("Segoe UI", 20, "bold"))
        
        style.configure("Subheader.TLabel",
                       background=AppStyles.BG_CARD,
                       foreground=AppStyles.TEXT_SECONDARY,
                       font=("Segoe UI", 11, "bold"))

        # Buttons
        style.configure("Accent.TButton",
                       background=AppStyles.ACCENT_PRIMARY,
                       foreground="white",
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       relief="flat",
                       padding=[28, 14])
        
        style.map("Accent.TButton",
                 background=[("active", AppStyles.ACCENT_SECONDARY), ("pressed", "#4f46e5")],
                 relief=[("pressed", "flat")])

        style.configure("Success.TButton",
                       background=AppStyles.ACCENT_SUCCESS,
                       foreground="white",
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       relief="flat",
                       padding=[28, 14])
        
        style.map("Success.TButton",
                 background=[("active", "#059669"), ("pressed", "#047857")],
                 relief=[("pressed", "flat")])
        
        style.configure("Warning.TButton",
                       background=AppStyles.ACCENT_WARNING,
                       foreground="white",
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       relief="flat",
                       padding=[28, 14])
        
        style.map("Warning.TButton",
                 background=[("active", "#d97706"), ("pressed", "#b45309")],
                 relief=[("pressed", "flat")])
        
        # Entry fields
        style.configure("TEntry",
                       fieldbackground=AppStyles.BG_ELEVATED,
                       foreground=AppStyles.TEXT_PRIMARY,
                       borderwidth=0,
                       relief="flat")
        
        # Progressbar
        style.configure("Custom.Horizontal.TProgressbar",
                       background=AppStyles.ACCENT_SUCCESS,
                       troughcolor=AppStyles.BG_ELEVATED,
                       borderwidth=0,
                       thickness=14)
