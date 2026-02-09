"""
SMTP Settings Dialog
"""
from tkinter import ttk, messagebox, scrolledtext
import tkinter as tk
from ..email_sender import EmailSender


class SMTPSettingsDialog:
    """SMTP Settings Configuration Dialog"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("SMTP Settings")
        self.dialog.geometry("550x650")
        self.dialog.configure(bg="#0a0a1a")
        self.dialog.resizable(True, True)
        
        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(self.dialog, bg="#0a0a1a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0e0e22")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20)
        
        # Main content frame
        main_frame = tk.Frame(scrollable_frame, bg="#0e0e22", padx=40, pady=40)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = tk.Label(
            main_frame,
            text="⚙️ SMTP Settings",
            font=("Segoe UI", 20, "bold"),
            fg="#6366f1",
            bg="#0e0e22"
        )
        header_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Configure your email server settings",
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg="#0e0e22"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Form
        form_frame = tk.Frame(main_frame, bg="#0e0e22")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # SMTP Server
        tk.Label(form_frame, text="SMTP Server:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=0, column=0, sticky="w", pady=12)
        
        self.server_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=35,
                                     bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                     relief="flat", bd=0, highlightthickness=2,
                                     highlightbackground="#252550", highlightcolor="#6366f1")
        self.server_entry.grid(row=0, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.server_entry.insert(0, self.app.config_manager.get("server", "smtp.gmail.com"))
        
        # Port
        tk.Label(form_frame, text="Port:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=1, column=0, sticky="w", pady=12)
        
        self.port_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=35,
                                   bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                   relief="flat", bd=0, highlightthickness=2,
                                   highlightbackground="#252550", highlightcolor="#6366f1")
        self.port_entry.grid(row=1, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.port_entry.insert(0, self.app.config_manager.get("port", "587"))
        
        # Email
        tk.Label(form_frame, text="Email:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=2, column=0, sticky="w", pady=12)
        
        self.email_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=35,
                                    bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                    relief="flat", bd=0, highlightthickness=2,
                                    highlightbackground="#252550", highlightcolor="#6366f1")
        self.email_entry.grid(row=2, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.email_entry.insert(0, self.app.config_manager.get("email", ""))
        
        # Password
        tk.Label(form_frame, text="Password:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=3, column=0, sticky="w", pady=12)
        
        self.password_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=35, show="●",
                                      bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                      relief="flat", bd=0, highlightthickness=2,
                                      highlightbackground="#252550", highlightcolor="#6366f1")
        self.password_entry.grid(row=3, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.password_entry.insert(0, self.app.config_manager.get("password", ""))
        
        # Reply-To
        tk.Label(form_frame, text="Reply-To:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=4, column=0, sticky="w", pady=12)
        
        self.reply_to_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=35,
                                       bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                       relief="flat", bd=0, highlightthickness=2,
                                       highlightbackground="#252550", highlightcolor="#6366f1")
        self.reply_to_entry.grid(row=4, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.reply_to_entry.insert(0, self.app.config_manager.get("reply_to", ""))
        
        tk.Label(form_frame, text="(Optional)", font=("Segoe UI", 9),
                fg="#9ca3af", bg="#0e0e22").grid(row=5, column=1, sticky="w", padx=(15, 0))
        
        # Delay
        tk.Label(form_frame, text="Delay (seconds):", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=6, column=0, sticky="w", pady=12)
        
        self.delay_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=35,
                                    bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                    relief="flat", bd=0, highlightthickness=2,
                                    highlightbackground="#252550", highlightcolor="#6366f1")
        self.delay_entry.grid(row=6, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.delay_entry.insert(0, self.app.config_manager.get("delay", "10"))
        
        tk.Label(form_frame, text="Time to wait between emails", font=("Segoe UI", 9),
                fg="#9ca3af", bg="#0e0e22").grid(row=7, column=1, sticky="w", padx=(15, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Info section
        info_frame = tk.Frame(main_frame, bg="#1a1a3a", relief="flat", bd=0)
        info_frame.pack(fill=tk.X, pady=(25, 20))
        
        info_label = tk.Label(
            info_frame,
            text="💡 Gmail Users: Use App Password, not your regular password\\n"
                 "   Generate at: myaccount.google.com/apppasswords",
            font=("Segoe UI", 9),
            fg="#06b6d4",
            bg="#1a1a3a",
            justify=tk.LEFT,
            padx=15,
            pady=12
        )
        info_label.pack(fill=tk.X)
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#0e0e22")
        btn_frame.pack(pady=(20, 0))
        
        # Save button
        save_btn = tk.Button(
            btn_frame,
            text="💾 Save",
            font=("Segoe UI", 11, "bold"),
            bg="#10b981",
            fg="#ffffff",
            activebackground="#059669",
            activeforeground="#ffffff",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.save_settings
        )
        save_btn.pack(side=tk.LEFT, padx=8)
        
        # Test button
        test_btn = tk.Button(
            btn_frame,
            text="🧪 Test Connection",
            font=("Segoe UI", 11, "bold"),
            bg="#6366f1",
            fg="#ffffff",
            activebackground="#4f46e5",
            activeforeground="#ffffff",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.test_connection
        )
        test_btn.pack(side=tk.LEFT, padx=8)
        
        # Close button
        close_btn = tk.Button(
            btn_frame,
            text="Close",
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="#9ca3af",
            activebackground="#334155",
            activeforeground="#f8fafc",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.dialog.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=8)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: (canvas.unbind_all("<MouseWheel>"), self.dialog.destroy()))
    
    def save_settings(self):
        """Save SMTP settings"""
        config = {
            "server": self.server_entry.get().strip(),
            "port": self.port_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "password": self.password_entry.get().strip(),
            "reply_to": self.reply_to_entry.get().strip(),
            "delay": self.delay_entry.get().strip()
        }
        
        if not all([config["server"], config["port"], config["email"]]):
            messagebox.showerror("Error", "❌ Server, Port, and Email are required!")
            return
        
        self.app.config_manager.update(config)
        if self.app.config_manager.save(self.app.config_manager.config):
            messagebox.showinfo("Success", "✅ Settings saved!")
        else:
            messagebox.showerror("Error", "❌ Failed to save settings")
    
    def test_connection(self):
        """Test SMTP connection"""
        server = self.server_entry.get().strip()
        port = self.port_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not all([server, port, email, password]):
            messagebox.showerror("Error", "❌ Please fill Server, Port, Email, and Password!")
            return
        
        try:
            email_sender = EmailSender(server, port, email, password)
            email_sender.test_connection()
            
            # Update app connection
            self.app.email_sender = email_sender
            self.app.is_connected = True
            self.app.update_connection_status(True)
            
            messagebox.showinfo("Success", "✅ Connection successful!")
        except Exception as e:
            self.app.is_connected = False
            self.app.update_connection_status(False)
            messagebox.showerror("Error", f"❌ Connection failed:\\n{str(e)}")
