"""
SMTP Settings Tab - Configure email server
"""
from tkinter import ttk, messagebox
import tkinter as tk
from .tab_base import TabBase
from ..email_sender import EmailSender


class SMTPTab(TabBase):
    """SMTP Configuration Tab"""
    
    def create_widgets(self):
        """Create SMTP settings widgets"""
        self.create_header(
            "⚙️ SMTP Configuration",
            "Configure your email server settings to start sending campaigns",
            "#6366f1"
        )
        
        card = ttk.Frame(self.frame, style="Card.TFrame", padding=40)
        card.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # SMTP Server
        ttk.Label(card, text="SMTP Server:", style="Subheader.TLabel").grid(row=0, column=0, sticky="w", pady=12)
        self.smtp_server = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.smtp_server.grid(row=0, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.smtp_server.insert(0, self.app.config_manager.get("server", "smtp.gmail.com"))
        
        # Port
        ttk.Label(card, text="SMTP Port:", style="Subheader.TLabel").grid(row=1, column=0, sticky="w", pady=12)
        self.smtp_port = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.smtp_port.grid(row=1, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.smtp_port.insert(0, self.app.config_manager.get("port", "587"))
        
        # Email
        ttk.Label(card, text="Your Email:", style="Subheader.TLabel").grid(row=2, column=0, sticky="w", pady=12)
        self.smtp_email = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.smtp_email.grid(row=2, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.smtp_email.insert(0, self.app.config_manager.get("email", ""))
        
        # Reply-To
        ttk.Label(card, text="Reply-To Email:", style="Subheader.TLabel").grid(row=3, column=0, sticky="w", pady=12)
        self.reply_to_email = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.reply_to_email.grid(row=3, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.reply_to_email.insert(0, self.app.config_manager.get("reply_to", ""))
        
        # Password
        ttk.Label(card, text="Password:", style="Subheader.TLabel").grid(row=4, column=0, sticky="w", pady=12)
        self.smtp_password = ttk.Entry(card, width=40, show="●", font=("Segoe UI", 11))
        self.smtp_password.grid(row=4, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.smtp_password.insert(0, self.app.config_manager.get("password", ""))
        
        # Delay
        ttk.Label(card, text="Delay (sec):", style="Subheader.TLabel").grid(row=5, column=0, sticky="w", pady=12)
        self.email_delay = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.email_delay.grid(row=5, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.email_delay.insert(0, self.app.config_manager.get("delay", "10"))
        
        # Buttons
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(40, 0))
        
        ttk.Button(btn_frame, text="💾 Save", command=self.save_config,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)
        
        ttk.Button(btn_frame, text="🧪 Test", command=self.test_connection,
                   style="Success.TButton").pack(side=tk.LEFT, padx=8)
        
        card.columnconfigure(1, weight=1)
    
    def save_config(self):
        """Save SMTP configuration"""
        config = {
            "server": self.smtp_server.get(),
            "port": self.smtp_port.get(),
            "email": self.smtp_email.get(),
            "reply_to": self.reply_to_email.get(),
            "password": self.smtp_password.get(),
            "delay": self.email_delay.get()
        }
        
        if self.app.config_manager.save(config):
            messagebox.showinfo("Success", "✅ Configuration saved!")
        else:
            messagebox.showerror("Error", "❌ Failed to save configuration")
    
    def test_connection(self):
        """Test SMTP connection"""
        try:
            email_sender = EmailSender(
                self.smtp_server.get(),
                self.smtp_port.get(),
                self.smtp_email.get(),
                self.smtp_password.get()
            )
            email_sender.test_connection()
            messagebox.showinfo("Success", "✅ Connection successful!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ {str(e)}")
