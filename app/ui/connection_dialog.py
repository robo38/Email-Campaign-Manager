"""
Connection Dialog for SMTP Authentication
"""
from tkinter import ttk, messagebox
import tkinter as tk
from ..email_sender import EmailSender


class ConnectionDialog:
    """SMTP Connection Dialog"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Connect to SMTP")
        self.dialog.geometry("550x550")
        self.dialog.configure(bg="#0a0a1a")
        self.dialog.resizable(True, True)  # Allow resizing
        
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
        
        # Main frame
        main_frame = tk.Frame(scrollable_frame, bg="#0e0e22", padx=40, pady=40)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = tk.Label(
            main_frame,
            text="🔌 Connect to SMTP Server",
            font=("Segoe UI", 18, "bold"),
            fg="#6366f1",
            bg="#0e0e22"
        )
        header_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Enter your credentials to connect",
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg="#0e0e22"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Form
        form_frame = tk.Frame(main_frame, bg="#0e0e22")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Email
        tk.Label(form_frame, text="Email:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=0, column=0, sticky="w", pady=12)
        
        self.email_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=30,
                                    bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                    relief="flat", bd=0, highlightthickness=2,
                                    highlightbackground="#252550", highlightcolor="#6366f1")
        self.email_entry.grid(row=0, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.email_entry.insert(0, self.app.config_manager.get("email", ""))
        
        # Password
        tk.Label(form_frame, text="Password:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=1, column=0, sticky="w", pady=12)
        
        self.password_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=30, show="●",
                                      bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                      relief="flat", bd=0, highlightthickness=2,
                                      highlightbackground="#252550", highlightcolor="#6366f1")
        self.password_entry.grid(row=1, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.password_entry.insert(0, self.app.config_manager.get("password", ""))
        
        # Server
        tk.Label(form_frame, text="SMTP Server:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=2, column=0, sticky="w", pady=12)
        
        self.server_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=30,
                                     bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                     relief="flat", bd=0, highlightthickness=2,
                                     highlightbackground="#252550", highlightcolor="#6366f1")
        self.server_entry.grid(row=2, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.server_entry.insert(0, self.app.config_manager.get("server", "smtp.gmail.com"))
        
        # Port
        tk.Label(form_frame, text="Port:", font=("Segoe UI", 11, "bold"),
                fg="#f8fafc", bg="#0e0e22").grid(row=3, column=0, sticky="w", pady=12)
        
        self.port_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=30,
                                   bg="#1a1a3a", fg="#f8fafc", insertbackground="#6366f1",
                                   relief="flat", bd=0, highlightthickness=2,
                                   highlightbackground="#252550", highlightcolor="#6366f1")
        self.port_entry.grid(row=3, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.port_entry.insert(0, self.app.config_manager.get("port", "587"))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#0e0e22")
        btn_frame.pack(pady=(30, 0))
        
        # Connect button
        connect_btn = tk.Button(
            btn_frame,
            text="🔌 Connect",
            font=("Segoe UI", 11, "bold"),
            bg="#6366f1",
            fg="#ffffff",
            activebackground="#4f46e5",
            activeforeground="#ffffff",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.connect
        )
        connect_btn.pack(side=tk.LEFT, padx=8)
        
        # Cancel button
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="#9ca3af",
            activebackground="#334155",
            activeforeground="#f8fafc",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.cancel
        )
        cancel_btn.pack(side=tk.LEFT, padx=8)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.connect())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: (canvas.unbind_all("<MouseWheel>"), self.cancel()))
    
    def connect(self):
        """Attempt connection"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        server = self.server_entry.get().strip()
        port = self.port_entry.get().strip()
        
        if not all([email, password, server, port]):
            messagebox.showerror("Error", "❌ Please fill all fields!")
            return
        
        try:
            # Test connection
            email_sender = EmailSender(server, port, email, password)
            email_sender.test_connection()
            
            # Save credentials
            config = {
                "email": email,
                "password": password,
                "server": server,
                "port": port
            }
            self.app.config_manager.update(config)
            self.app.config_manager.save(self.app.config_manager.config)
            
            # Update app state
            self.app.email_sender = email_sender
            self.app.is_connected = True
            self.app.update_connection_status(True)
            
            messagebox.showinfo("Success", "✅ Connection successful!")
            self.dialog.destroy()
            
        except Exception as e:
            self.app.is_connected = False
            self.app.update_connection_status(False)
            messagebox.showerror("Error", f"❌ Connection failed:\n{str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.dialog.destroy()
