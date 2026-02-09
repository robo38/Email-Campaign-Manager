"""
Email Campaign Manager - Main Entry Point
Run this file to start the application
"""
import tkinter as tk
from app.ui.main_window import BulkEmailSender


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = BulkEmailSender(root)
    root.mainloop()


if __name__ == "__main__":
    main()
