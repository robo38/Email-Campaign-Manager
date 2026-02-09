"""
=======================================================================
LEGACY VERSION - ORIGINAL MONOLITHIC FILE (Still works!)
=======================================================================

⚠️  NOTE: This is the original 1354-line monolithic version of the app.
    It still works perfectly fine if you prefer a single-file solution.

✨  NEW VERSION: For the modern, modular version with better organization:
    Run: python main.py

📁  The new structure separates:
    - Business logic (app/config.py, app/email_sender.py)
    - UI components (app/ui/*.py)  
    - Templates (templates/*.html, *.css)
    - Configuration (config/smtp_config.json)
    - Data files (data/*.csv)

Both versions have the same features and functionality!

=======================================================================
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import csv
import json
import os
import time
import random
from datetime import datetime
import re
from html.parser import HTMLParser
import tempfile
import webbrowser


class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_style = False
        self.in_script = False

    def handle_starttag(self, tag, attrs):
        if tag == 'style':
            self.in_style = True
        elif tag == 'script':
            self.in_script = True
        elif tag == 'a':
            self.text.append("[Link: ")
        elif tag == 'br':
            self.text.append('\n')
        elif tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol', 'tr']:
            if self.text and self.text[-1] != '\n':
                 self.text.append('\n')

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
        elif tag == 'script':
            self.in_script = False
        elif tag == 'a':
             self.text.append("] ")
        elif tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol', 'tr']:
            self.text.append('\n')

    def handle_data(self, data):
        if not self.in_style and not self.in_script:
            clean_data = data.strip()
            if clean_data:
                self.text.append(clean_data + ' ')

class BulkEmailSender:
    def __init__(self, root):
        self.root = root
        self.root.title("✉️ Professional Email Campaign Manager")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a1a")
        self.config_file = "smtp_config.json"
        self.smtp_config = self.load_smtp_config()
        self.temp_html_file = None
        self.embedded_images = {}  # Store embedded images as {name: path}
        self.is_connected = False
        self.connection_status_label = None
        self.setup_styles()
        
        # Create main container first (needed for toolbar placement)
        main_container = ttk.Frame(root, style="Main.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        # Now create toolbar (will be placed before main_container)
        self.create_top_toolbar()

        self.notebook = ttk.Notebook(main_container, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.create_smtp_tab()
        self.create_recipients_tab()
        self.create_send_tab()
        self.create_compose_tab()
        self.notebook.add(self.smtp_frame, text="  ⚙️  SMTP Settings  ")
        self.notebook.add(self.recipients_frame, text="  👥  Recipients  ")
        self.notebook.add(self.compose_frame, text="  ✍️  Compose  ")
        self.notebook.add(self.send_frame, text="  🚀  Send  ")
        self.HTMLTextExtractor = HTMLTextExtractor
        self.schedule_preview_update()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Ultra-modern color palette with depth
        bg_dark = "#0a0a1a"          # Deep background
        bg_card = "#13132b"           # Card background
        bg_elevated = "#1a1a3a"       # Input backgrounds
        bg_hover = "#252550"          # Hover states
        
        # Vibrant accent colors
        accent_primary = "#6366f1"    # Indigo with glow
        accent_secondary = "#06b6d4"  # Cyan
        accent_success = "#10b981"    # Emerald
        accent_warning = "#f59e0b"    # Amber
        accent_error = "#ef4444"      # Red
        
        # Text colors with hierarchy
        text_primary = "#f8fafc"
        text_secondary = "#cbd5e1"
        text_muted = "#94a3b8"
        
        # Main container with shadow effect
        style.configure("Main.TFrame", background=bg_dark)
        
        # Modern Notebook (Tabs) with elevation
        style.configure("TNotebook", 
                       background=bg_dark, 
                       borderwidth=0,
                       tabmargins=[15, 10, 15, 0])
        
        style.configure("TNotebook.Tab",
                       background=bg_card,
                       foreground=text_muted,
                       padding=[28, 14],
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0)
        
        style.map("TNotebook.Tab",
                 background=[("selected", bg_elevated)],
                 foreground=[("selected", text_primary)],
                 padding=[("selected", [28, 14])],
                 relief=[("selected", "flat")])

        # Card frames with modern look
        style.configure("Card.TFrame", 
                       background=bg_card, 
                       relief="flat",
                       borderwidth=0)

        # Labels with better contrast
        style.configure("TLabel",
                       background=bg_card,
                       foreground=text_primary,
                       font=("Segoe UI", 10))
        
        style.configure("Header.TLabel",
                       background=bg_card,
                       foreground=text_primary,
                       font=("Segoe UI", 20, "bold"))
        
        style.configure("Subheader.TLabel",
                       background=bg_card,
                       foreground=text_secondary,
                       font=("Segoe UI", 11, "bold"))

        # Modern Buttons with glow effect
        style.configure("Accent.TButton",
                       background=accent_primary,
                       foreground="white",
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       relief="flat",
                       padding=[28, 14])
        
        style.map("Accent.TButton",
                 background=[("active", accent_secondary), ("pressed", "#4f46e5")],
                 relief=[("pressed", "flat")])

        # Success Button with shine
        style.configure("Success.TButton",
                       background=accent_success,
                       foreground="white",
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       relief="flat",
                       padding=[28, 14])
        
        style.map("Success.TButton",
                 background=[("active", "#059669"), ("pressed", "#047857")],
                 relief=[("pressed", "flat")])
        
        # Warning Button
        style.configure("Warning.TButton",
                       background=accent_warning,
                       foreground="white",
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       relief="flat",
                       padding=[28, 14])
        
        style.map("Warning.TButton",
                 background=[("active", "#d97706"), ("pressed", "#b45309")],
                 relief=[("pressed", "flat")])
        
        # Entry fields with modern look
        style.configure("TEntry",
                       fieldbackground=bg_elevated,
                       foreground=text_primary,
                       borderwidth=0,
                       relief="flat")
        
        # Animated Progressbar
        style.configure("Custom.Horizontal.TProgressbar",
                       background=accent_success,
                       troughcolor=bg_elevated,
                       borderwidth=0,
                       thickness=14)
    
    def create_top_toolbar(self):
        """Create a modern top toolbar with connection status"""
        toolbar = tk.Frame(self.root, bg="#13132b", height=65)
        toolbar.pack(fill=tk.X, side=tk.TOP, before=self.root.winfo_children()[0])
        
        # Add subtle separator line
        separator = tk.Frame(toolbar, bg="#252550", height=1)
        separator.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Left side - Connection button
        left_frame = tk.Frame(toolbar, bg="#13132b")
        left_frame.pack(side=tk.LEFT, padx=25, pady=12)
        
        # Connection status indicator with glow
        self.connection_indicator = tk.Canvas(left_frame, width=14, height=14, bg="#13132b", highlightthickness=0)
        self.connection_indicator.pack(side=tk.LEFT, padx=(0, 12))
        self.connection_circle = self.connection_indicator.create_oval(2, 2, 12, 12, fill="#64748b", outline="")
        
        # Modern connection button with hover effect
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
        
        # Bind hover effects
        self.connection_btn.bind("<Enter>", lambda e: self.connection_btn.config(bg="#4f46e5"))
        self.connection_btn.bind("<Leave>", lambda e: self.connection_btn.config(bg="#6366f1" if not self.is_connected else "#10b981"))
        
        # Connection status label
        self.connection_status_label = tk.Label(
            left_frame,
            text="Not Connected",
            bg="#13132b",
            fg="#94a3b8",
            font=("Segoe UI", 10)
        )
        self.connection_status_label.pack(side=tk.LEFT, padx=15)
        
        # Right side - App info with gradient effect
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
        
        # Check if already connected from saved config
        if self.smtp_config.get("server") and self.smtp_config.get("email") and self.smtp_config.get("password"):
            self.test_and_connect_auto()
    
    def show_connection_dialog(self):
        """Show a modern popup dialog for SMTP connection"""
        dialog = tk.Toplevel(self.root)
        dialog.title("SMTP Connection")
        dialog.geometry("500x400")
        dialog.configure(bg="#0f0f1e")
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg="#1a1a2e", height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="🔌 SMTP Connection",
            bg="#1a1a2e",
            fg="#f1f5f9",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=15)
        
        # Content
        content = tk.Frame(dialog, bg="#0f0f1e")
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Server
        tk.Label(content, text="SMTP Server:", bg="#0f0f1e", fg="#f8fafc", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 5))
        server_entry = tk.Entry(content, bg="#1a1a3a", fg="#f8fafc", font=("Segoe UI", 11), relief="flat", insertbackground="#6366f1", borderwidth=0, highlightthickness=2, highlightbackground="#252550", highlightcolor="#6366f1")
        server_entry.pack(fill=tk.X, ipady=10, pady=(0, 10))
        server_entry.insert(0, self.smtp_server.get())
        
        # Port
        tk.Label(content, text="Port:", bg="#0f0f1e", fg="#f8fafc", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5, 5))
        port_entry = tk.Entry(content, bg="#1a1a3a", fg="#f8fafc", font=("Segoe UI", 11), relief="flat", insertbackground="#6366f1", borderwidth=0, highlightthickness=2, highlightbackground="#252550", highlightcolor="#6366f1")
        port_entry.pack(fill=tk.X, ipady=10, pady=(0, 10))
        port_entry.insert(0, self.smtp_port.get())
        
        # Email
        tk.Label(content, text="Email:", bg="#0f0f1e", fg="#f8fafc", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5, 5))
        email_entry = tk.Entry(content, bg="#1a1a3a", fg="#f8fafc", font=("Segoe UI", 11), relief="flat", insertbackground="#6366f1", borderwidth=0, highlightthickness=2, highlightbackground="#252550", highlightcolor="#6366f1")
        email_entry.pack(fill=tk.X, ipady=10, pady=(0, 10))
        email_entry.insert(0, self.smtp_email.get())
        
        # Password
        tk.Label(content, text="Password:", bg="#0f0f1e", fg="#f8fafc", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5, 5))
        password_entry = tk.Entry(content, bg="#1a1a3a", fg="#f8fafc", font=("Segoe UI", 11), show="●", relief="flat", insertbackground="#6366f1", borderwidth=0, highlightthickness=2, highlightbackground="#252550", highlightcolor="#6366f1")
        password_entry.pack(fill=tk.X, ipady=10, pady=(0, 15))
        password_entry.insert(0, self.smtp_password.get())
        
        # Buttons
        btn_frame = tk.Frame(content, bg="#0f0f1e")
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        def connect():
            # Update main form
            self.smtp_server.delete(0, tk.END)
            self.smtp_server.insert(0, server_entry.get())
            self.smtp_port.delete(0, tk.END)
            self.smtp_port.insert(0, port_entry.get())
            self.smtp_email.delete(0, tk.END)
            self.smtp_email.insert(0, email_entry.get())
            self.smtp_password.delete(0, tk.END)
            self.smtp_password.insert(0, password_entry.get())
            
            # Test connection
            try:
                server = smtplib.SMTP(server_entry.get(), int(port_entry.get()))
                server.starttls()
                server.login(email_entry.get(), password_entry.get())
                server.quit()
                
                self.is_connected = True
                self.update_connection_status(True)
                self.save_smtp_config()
                
                messagebox.showinfo("Success", "✅ Connected successfully!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"❌ Connection failed: {str(e)}")
        
        tk.Button(
            btn_frame,
            text="Connect",
            bg="#10b981",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground="#059669",
            activeforeground="white",
            command=connect
        ).pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            bg="#475569",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground="#334155",
            activeforeground="white",
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def test_and_connect_auto(self):
        """Test connection automatically with saved credentials"""
        try:
            server = smtplib.SMTP(self.smtp_server.get(), int(self.smtp_port.get()))
            server.starttls()
            server.login(self.smtp_email.get(), self.smtp_password.get())
            server.quit()
            self.is_connected = True
            self.update_connection_status(True)
        except:
            self.is_connected = False
            self.update_connection_status(False)
    
    def update_connection_status(self, connected):
        """Update the connection status indicator"""
        if connected:
            self.connection_indicator.itemconfig(self.connection_circle, fill="#10b981")
            self.connection_status_label.config(text="✓ Connected", fg="#10b981", font=("Segoe UI", 10, "bold"))
            self.connection_btn.config(text="✅ Connected", bg="#10b981")
            # Bind hover for connected state
            self.connection_btn.bind("<Leave>", lambda e: self.connection_btn.config(bg="#10b981"))
        else:
            self.connection_indicator.itemconfig(self.connection_circle, fill="#64748b")
            self.connection_status_label.config(text="Not Connected", fg="#94a3b8", font=("Segoe UI", 10))
            self.connection_btn.config(text="🔌 Connect SMTP", bg="#6366f1")
            # Bind hover for disconnected state
            self.connection_btn.bind("<Leave>", lambda e: self.connection_btn.config(bg="#6366f1"))

    def create_smtp_tab(self):
        smtp_frame = ttk.Frame(self.notebook, style="Main.TFrame")
        self.smtp_frame = smtp_frame
        
        # Add gradient-like header bar
        header_frame = ttk.Frame(smtp_frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 0))
        
        # Add subtle top border accent
        accent_line = tk.Frame(header_frame, bg="#6366f1", height=3)
        accent_line.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="⚙️ SMTP Configuration", 
                 style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(header_frame, text="Configure your email server settings to start sending campaigns",
                 foreground="#94a3b8", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 20))
        
        card = ttk.Frame(smtp_frame, style="Card.TFrame", padding=40)
        card.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        ttk.Label(card, text="SMTP Server:", style="Subheader.TLabel").grid(row=1, column=0, sticky="w", pady=12)
        self.smtp_server = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.smtp_server.grid(row=1, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.smtp_server.insert(0, self.smtp_config.get("server", "smtp.gmail.com"))

        ttk.Label(card, text="SMTP Port:", style="Subheader.TLabel").grid(row=2, column=0, sticky="w", pady=12)
        self.smtp_port = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.smtp_port.grid(row=2, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.smtp_port.insert(0, self.smtp_config.get("port", "587"))

        ttk.Label(card, text="Your Email:", style="Subheader.TLabel").grid(row=3, column=0, sticky="w", pady=12)
        self.smtp_email = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.smtp_email.grid(row=3, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.smtp_email.insert(0, self.smtp_config.get("email", ""))

        ttk.Label(card, text="Reply-To Email:", style="Subheader.TLabel").grid(row=4, column=0, sticky="w", pady=12)
        self.reply_to_email = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.reply_to_email.grid(row=4, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.reply_to_email.insert(0, self.smtp_config.get("reply_to", ""))

        ttk.Label(card, text="Password/App Password:", style="Subheader.TLabel").grid(row=5, column=0, sticky="w", pady=12)
        self.smtp_password = ttk.Entry(card, width=40, show="●", font=("Segoe UI", 11))
        self.smtp_password.grid(row=5, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.smtp_password.insert(0, self.smtp_config.get("password", ""))

        ttk.Label(card, text="Delay Between Batches (sec):", style="Subheader.TLabel").grid(row=6, column=0, sticky="w", pady=12)
        self.email_delay = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        self.email_delay.grid(row=6, column=1, sticky="ew", pady=12, padx=(15, 0))
        self.email_delay.insert(0, self.smtp_config.get("delay", "10"))

        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=(40, 0))

        ttk.Button(btn_frame, text="💾 Save Configuration",
                   command=self.save_smtp_config,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)

        ttk.Button(btn_frame, text="🧪 Test Connection",
                   command=self.test_smtp_connection,
                   style="Success.TButton").pack(side=tk.LEFT, padx=8)

        card.columnconfigure(1, weight=1)

        # Info box with modern styling
        info_frame = ttk.Frame(card, style="Card.TFrame")
        info_frame.grid(row=8, column=0, columnspan=2, pady=(30, 0), sticky="ew")
        
        info_text = "💡 Tip: Use App Passwords for Gmail/Outlook for better security and deliverability"
        info_label = ttk.Label(info_frame, text=info_text, foreground="#f59e0b", 
                             font=("Segoe UI", 10), wraplength=600)
        info_label.pack(pady=15, padx=20)

    def create_compose_tab(self):
        compose_frame = ttk.Frame(self.notebook, style="Main.TFrame")
        self.compose_frame = compose_frame

        # Add header section
        header_frame = ttk.Frame(compose_frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        # Add accent line
        accent_line = tk.Frame(header_frame, bg="#f59e0b", height=3)
        accent_line.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(header_frame, text="✍️ Compose Email", 
                 style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(header_frame, text="Design your email template with HTML and live preview",
                 foreground="#94a3b8", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 15))

        main_container = ttk.Frame(compose_frame, style="Main.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_container, style="Card.TFrame", padding=25)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        header = ttk.Label(left_frame, text="Email Content", style="Subheader.TLabel")
        header.pack(anchor="w", pady=(0, 20))

        subject_frame = ttk.Frame(left_frame, style="Card.TFrame")
        subject_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(subject_frame, text="Subject Line:", style="Subheader.TLabel").pack(anchor="w")
        self.email_subject = ttk.Entry(subject_frame, font=("Segoe UI", 11))
        self.email_subject.pack(fill=tk.X, pady=(8, 0))

        html_frame = ttk.Frame(left_frame, style="Card.TFrame")
        html_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        ttk.Label(html_frame, text="HTML Template:", style="Subheader.TLabel").pack(anchor="w")

        self.html_editor = scrolledtext.ScrolledText(
            html_frame,
            wrap=tk.WORD,
            font=("JetBrains Mono", 10),
            bg="#1a1a3a",
            fg="#f8fafc",
            insertbackground="#6366f1",
            relief="flat",
            padx=18,
            pady=18,
            borderwidth=0,
            highlightthickness=2,
            highlightbackground="#252550",
            highlightcolor="#6366f1"
        )
        self.html_editor.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        # Remove default 'a' binding and only allow Ctrl+A / Cmd+A
        self.html_editor.bind("<Key>", lambda e: None if e.keysym == 'a' and not (e.state & 0x4 or e.state & 0x8) else None)
        self.html_editor.bind("<Control-a>", self.select_all_text)
        self.html_editor.bind("<Command-a>", self.select_all_text)

        btn_frame_left = ttk.Frame(left_frame, style="Card.TFrame")
        btn_frame_left.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_frame_left, text="📄 Load Template",
                   command=self.load_html_template,
                   style="Success.TButton").pack(side=tk.LEFT, padx=8)
        
        ttk.Button(btn_frame_left, text="🖼️ Upload Images",
                   command=self.upload_images,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)
        
        ttk.Button(btn_frame_left, text="🗑️ Clear Images",
                   command=self.clear_images,
                   style="Warning.TButton").pack(side=tk.LEFT, padx=8)
        
        # Display embedded images with CID references
        images_info_frame = ttk.Frame(left_frame, style="Card.TFrame")
        images_info_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Label(images_info_frame, text="Uploaded Images (copy tags to use in HTML):", 
                  style="Subheader.TLabel", foreground="#0ea5e9").pack(anchor="w")
        
        self.images_text = scrolledtext.ScrolledText(
            images_info_frame,
            wrap=tk.WORD,
            font=("JetBrains Mono", 9),
            bg="#0a0a1a",
            fg="#10b981",
            height=4,
            relief="flat",
            padx=18,
            pady=12,
            borderwidth=0,
            highlightthickness=2,
            highlightbackground="#252550"
        )
        self.images_text.pack(fill=tk.X, pady=(8, 0))
        self.images_text.insert("1.0", "No images uploaded. Click 'Upload Images' to add images for your template.")
        self.images_text.config(state='disabled')

        right_frame = ttk.Frame(main_container, style="Card.TFrame", padding=25)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        preview_header = ttk.Label(right_frame, text="Live Preview", style="Subheader.TLabel")
        preview_header.pack(anchor="w", pady=(0, 20))

        preview_container = ttk.Frame(right_frame, style="Card.TFrame")
        preview_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create a frame to mimic browser window
        browser_frame = tk.Frame(preview_container, bg="#e2e8f0", relief="flat")
        browser_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Browser-like title bar
        title_bar = tk.Frame(browser_frame, bg="#cbd5e1", height=30)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)
        
        # Browser dots
        dots_frame = tk.Frame(title_bar, bg="#cbd5e1")
        dots_frame.pack(side=tk.LEFT, padx=10, pady=8)
        for color in ["#ef4444", "#f59e0b", "#10b981"]:
            tk.Canvas(dots_frame, width=12, height=12, bg="#cbd5e1", highlightthickness=0).pack(side=tk.LEFT, padx=2)
            dots_frame.winfo_children()[-1].create_oval(2, 2, 10, 10, fill=color, outline="")
        
        tk.Label(title_bar, text="Email Preview", bg="#cbd5e1", fg="#475569", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=10)

        self.preview_display = scrolledtext.ScrolledText(
            browser_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg="white",
            fg="#1e293b",
            insertbackground="#4f46e5",
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=20,
            state='disabled'
        )
        self.preview_display.pack(fill=tk.BOTH, expand=True)

        btn_frame_right = ttk.Frame(right_frame, style="Card.TFrame")
        btn_frame_right.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_frame_right, text="🌐 Open in Browser",
                   command=self.preview_email,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)


        # Default HTML template
        default_html = """<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; }
        .button { background: #667eea; color: white; padding: 12px 30px;
                  text-decoration: none; border-radius: 5px; display: inline-block; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
        .embedded-image { max-width: 100%; height: auto; display: block; margin: 20px auto; }
        .qrcode { width: 200px; height: 200px; margin: 20px auto; display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Hello {{name}}!</h1>
        </div>
        <div class="content">
            <p>This is your personalized email message.</p>
            <p>You can customize this template with HTML and CSS.</p>
            
            <!-- Example: Upload images and use them like this -->
            <!-- <img src="cid:your_image_name" class="embedded-image" alt="Your Image"> -->
            
            <!-- QR Code from CSV (use {{qrcode}} placeholder) -->
            <!-- <img src="cid:{{qrcode}}" class="qrcode" alt="Your QR Code"> -->
            
            <p style="text-align: center; margin: 30px 0;">
                <a href="{{link}}" class="button">Call to Action</a>
            </p>
            <ul><li>Item 1</li><li>Item 2</li></ul>
        </div>
        <div class="footer">
            <p>© 2025 Your Company. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
        self.html_editor.insert("1.0", default_html)

        self.update_text_preview()

    def select_all_text(self, event):
        event.widget.event_generate("<<SelectAll>>")
        return "break"
    
    def upload_images(self):
        """Allow user to upload images and get CID references for HTML"""
        filenames = filedialog.askopenfilenames(
            title="Select Images to Embed in Email",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if filenames:
            for filepath in filenames:
                # Use filename without extension as the CID name
                filename = os.path.basename(filepath)
                name_without_ext = os.path.splitext(filename)[0]
                # Clean name for CID (remove spaces and special chars)
                cid_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name_without_ext)
                
                # Store with unique name if duplicate
                counter = 1
                original_cid = cid_name
                while cid_name in self.embedded_images:
                    cid_name = f"{original_cid}_{counter}"
                    counter += 1
                
                self.embedded_images[cid_name] = filepath
            
            self.update_images_display()
            messagebox.showinfo("Success", f"✅ {len(filenames)} image(s) uploaded!")
    
    def clear_images(self):
        """Clear all embedded images"""
        if self.embedded_images and messagebox.askyesno("Confirm", "Clear all uploaded images?"):
            self.embedded_images = {}
            self.update_images_display()
    
    def update_images_display(self):
        """Update the text showing how to use embedded images"""
        self.images_text.config(state='normal')
        self.images_text.delete("1.0", tk.END)
        
        if self.embedded_images:
            self.images_text.insert("1.0", "✨ Copy these tags and paste into your HTML template:\n\n")
            for cid_name, filepath in self.embedded_images.items():
                filename = os.path.basename(filepath)
                img_tag = f'<img src="cid:{cid_name}" alt="{filename}">'
                self.images_text.insert(tk.END, f"{img_tag}\n")
            self.images_text.insert(tk.END, f"\n💡 Tip: Add width/height attributes for better control")
        else:
            self.images_text.insert("1.0", "🖼️ No images uploaded yet.\nClick 'Upload Images' to add images for your email template.")
        
        self.images_text.config(state='disabled')

    def create_recipients_tab(self):
        recipients_frame = ttk.Frame(self.notebook, style="Main.TFrame")
        self.recipients_frame = recipients_frame

        # Header section
        header_frame = ttk.Frame(recipients_frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 0))
        
        # Add accent line
        accent_line = tk.Frame(header_frame, bg="#06b6d4", height=3)
        accent_line.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="👥 Manage Recipients", 
                 style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(header_frame, text="Import or add recipients for your email campaign",
                 foreground="#94a3b8", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 20))

        card = ttk.Frame(recipients_frame, style="Card.TFrame", padding=40)
        card.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        import_frame = ttk.Frame(card, style="Card.TFrame")
        import_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Button(import_frame, text="📂 Import CSV",
                   command=lambda: self.import_recipients("csv"),
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)

        ttk.Button(import_frame, text="📄 Import TXT",
                   command=lambda: self.import_recipients("txt"),
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)

        ttk.Button(import_frame, text="🗑️ Clear All",
                   command=self.clear_recipients,
                   style="Warning.TButton").pack(side=tk.LEFT, padx=8)

        ttk.Label(card, text="Recipients List:",
                  style="Subheader.TLabel").pack(anchor="w", pady=(15, 8))

        self.recipients_text = scrolledtext.ScrolledText(
            card,
            wrap=tk.WORD,
            font=("JetBrains Mono", 10),
            bg="#1a1a3a",
            fg="#f8fafc",
            insertbackground="#6366f1",
            relief="flat",
            padx=18,
            pady=18,
            height=15,
            borderwidth=0,
            highlightthickness=2,
            highlightbackground="#252550",
            highlightcolor="#6366f1"
        )
        self.recipients_text.pack(fill=tk.BOTH, expand=True)

        # Info
        info_frame = ttk.Frame(card, style="Card.TFrame")
        info_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Label(info_frame, text="💡 Supported Formats:", 
                 foreground="#0ea5e9", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 5))
        
        format1 = "   • Simple: email@example.com"
        format2 = "   • With name: email@example.com,John Doe"
        format3 = "   • With link: email@example.com,John Doe,https://link.com"
        format4 = "   • CSV with QR: id,email,QRCode_Image,Name (or upload CSV file)"
        
        for fmt in [format1, format2, format3, format4]:
            ttk.Label(info_frame, text=fmt, foreground="#f59e0b", 
                     font=("JetBrains Mono", 9)).pack(anchor="w", pady=2)

    def create_send_tab(self):
        send_frame = ttk.Frame(self.notebook, style="Main.TFrame")
        self.send_frame = send_frame

        # Header section
        header_frame = ttk.Frame(send_frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 0))
        
        # Add accent line
        accent_line = tk.Frame(header_frame, bg="#10b981", height=3)
        accent_line.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="🚀 Send Campaign", 
                 style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(header_frame, text="Monitor your email campaign progress in real-time",
                 foreground="#94a3b8", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 20))

        card = ttk.Frame(send_frame, style="Card.TFrame", padding=40)
        card.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            card,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar",
            length=500
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 25))
        self.status_text = scrolledtext.ScrolledText(
            card,
            wrap=tk.WORD,
            font=("JetBrains Mono", 9),
            bg="#1a1a3a",
            fg="#cbd5e1",
            insertbackground="#6366f1",
            relief="flat",
            padx=18,
            pady=18,
            height=20,
            borderwidth=0,
            highlightthickness=2,
            highlightbackground="#252550"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.send_button = ttk.Button(
            card,
            text="🚀 Start Sending Campaign",
            command=self.send_bulk_email,
            style="Success.TButton"
        )
        self.send_button.pack(pady=20)


    def update_text_preview(self):
        try:
            html_content = self.html_editor.get("1.0", tk.END).strip()
            # Replace placeholders with preview values
            html_content = html_content.replace("{{name}}", "John Doe")
            html_content = html_content.replace("{{link}}", "#")
            html_content = html_content.replace("{{qrcode}}", "qrcode-preview")

            parser = self.HTMLTextExtractor()
            parser.feed(html_content)

            preview_text = ''.join(parser.text)
            preview_text = re.sub(r'[\s]{2,}', ' ', preview_text).strip()
            preview_text = preview_text.replace('\n ', '\n').replace(' \n', '\n')
            
            # Add visual enhancements to preview
            enhanced_preview = self.enhance_preview_text(preview_text, html_content)

            self.preview_display.config(state='normal')
            self.preview_display.delete("1.0", tk.END)
            
            # Configure text tags for styling
            self.preview_display.tag_configure("header", font=("Segoe UI", 16, "bold"), foreground="#5b21b6")
            self.preview_display.tag_configure("subheader", font=("Segoe UI", 12, "bold"), foreground="#4338ca")
            self.preview_display.tag_configure("link", font=("Segoe UI", 10, "underline"), foreground="#2563eb")
            self.preview_display.tag_configure("button", font=("Segoe UI", 10, "bold"), foreground="white", background="#4f46e5")
            self.preview_display.tag_configure("regular", font=("Segoe UI", 10), foreground="#334155")
            self.preview_display.tag_configure("footer", font=("Segoe UI", 8), foreground="#64748b")
            
            self.preview_display.insert("1.0", enhanced_preview)
            self.apply_preview_styling(html_content)
            
            self.preview_display.config(state='disabled')

        except Exception as e:
            pass
    
    def enhance_preview_text(self, text, html):
        """Enhance the preview text with better formatting"""
        # Add visual separators
        lines = text.split('\n')
        enhanced = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Detect headers
                if any(tag in html for tag in ['<h1>', '<h2>', '<h3>']):
                    if len(line) < 50 and not line.endswith('.'):
                        enhanced.append(f"\n{'═' * 50}")
                        enhanced.append(line)
                        enhanced.append(f"{'═' * 50}\n")
                        continue
                enhanced.append(line)
        
        return '\n\n'.join(enhanced)
    
    def apply_preview_styling(self, html):
        """Apply styling to preview based on HTML content"""
        content = self.preview_display.get("1.0", tk.END)
        
        # Style headers
        for i, line in enumerate(content.split('\n')):
            line = line.strip()
            if line and len(line) < 50 and ('Hello' in line or 'Welcome' in line):
                start_idx = content.find(line)
                if start_idx != -1:
                    end_idx = start_idx + len(line)
                    self.preview_display.tag_add("header", f"1.0+{start_idx}c", f"1.0+{end_idx}c")


    def _update_temp_file(self):
        if not self.temp_html_file or not os.path.exists(self.temp_html_file):
            return

        html_content = self.html_editor.get("1.0", tk.END)
        html_content = html_content.replace("{{name}}", "Preview User")
        try:
            with open(self.temp_html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            self.log_status(f"❌ Error writing to temp file: {str(e)}")


    def preview_email(self):
        html_content = self.html_editor.get("1.0", tk.END)
        html_content = html_content.replace("{{name}}", "Preview User")

        if not self.temp_html_file or not os.path.exists(self.temp_html_file):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                f.write(html_content)
                self.temp_html_file = f.name

            webbrowser.open('file://' + self.temp_html_file, new=0)
            self.log_status(f"🌐 Opened live preview in browser: {self.temp_html_file}")
        else:
            self._update_temp_file()
            webbrowser.open('file://' + self.temp_html_file, new=0)


    def schedule_preview_update(self):
        self.update_text_preview()
        if self.temp_html_file and os.path.exists(self.temp_html_file):
            self._update_temp_file()
        self.root.after(1000, self.schedule_preview_update)

    def _remove_beefree_watermark(self, html_content):
        """
        Removes the specific <tr> block containing the "Designed with Beefree" watermark
        and the Beefree logo image from the HTML content.
        """

        pattern = re.compile(
            r'<tr>.*?Beefree-logo\.png.*?</tr>',
            re.IGNORECASE | re.DOTALL
        )

        cleaned_html = pattern.sub('', html_content)

        pattern_2 = re.compile(
            r'<table.*?designedwithbeefree\.com.*?</table>',
            re.IGNORECASE | re.DOTALL
        )
        cleaned_html = pattern_2.sub('', cleaned_html)

        return cleaned_html

    def _chunk_list(self, recipients_list, chunk_size):
        """Yield successive n-sized chunks from list."""
        for i in range(0, len(recipients_list), chunk_size):
            yield recipients_list[i:i + chunk_size]

    def send_bulk_email(self):
        """Send bulk emails using batching and BCC."""
        if not self.smtp_server.get() or not self.smtp_email.get() or not self.smtp_password.get():
            messagebox.showerror("Error", "❌ Please configure SMTP settings first!")
            return

        # Use default subject if empty
        subject = self.email_subject.get().strip()
        if not subject:
            subject = f"Important Message - {datetime.now().strftime('%B %d, %Y')}"
            self.email_subject.delete(0, tk.END)
            self.email_subject.insert(0, subject)

        recipients_data = self.parse_recipients()
        recipient_emails = [r['email'] for r in recipients_data]

        if not recipient_emails:
            messagebox.showerror("Error", "❌ No valid recipients found!")
            return

        if not messagebox.askyesno("Confirm",
                                   f"Send email to {len(recipient_emails)} recipients in batches?"):
            return

        self.send_button.config(state="disabled")
        self.status_text.delete("1.0", tk.END)
        self.log_status(f"📧 Starting campaign for {len(recipient_emails)} recipients...")

        try:
            delay = float(self.email_delay.get())
            if delay < 5:
                delay = 5
        except:
            delay = 10

        BATCH_SIZE = 100

        original_html_content = self.html_editor.get("1.0", tk.END)
        cleaned_html_content = self._remove_beefree_watermark(original_html_content)

        server = None
        total_sent = 0
        total_batches = 0

        try:
            server = smtplib.SMTP(self.smtp_server.get(), int(self.smtp_port.get()))
            server.starttls()
            server.login(self.smtp_email.get(), self.smtp_password.get())

            # batches = list(self._chunk_list(recipient_emails, BATCH_SIZE))
            batches = list(self._chunk_list(recipient_emails, 1))
            total_batches = len(batches)

            # تحديد عنوان الرد (Reply-To)
            reply_to = self.reply_to_email.get().strip()
            if not reply_to:
                # إذا تُرك فارغاً، استخدم بريد الإرسال (Your Email)
                reply_to = self.smtp_email.get()

            # تحديد محتوى الرسالة النهائي (مع إزالة التخصيص)
            # final_html_content = cleaned_html_content.replace("{{name}}", recipients_data[0]['name'] if recipients_data else "Valued Customer")
            self.log_status(f"{[recipients_data[i]['name'] for i in range(len(batches))]}")


            for batch_idx, batch in enumerate(batches):
                self.log_status(f"Sending Batch {batch_idx + 1} of {total_batches} (Recipients: {len(batch)})...")
                
                # Get recipient data for this batch
                recipient_data = recipients_data[batch_idx] if batch_idx < len(recipients_data) else {}
                
                # Replace template variables
                temp_html = cleaned_html_content.replace("{{name}}", recipient_data.get('name', 'Valued Customer'))
                temp_html = temp_html.replace("{{link}}", recipient_data.get('link', '#'))
                
                # Check if recipient has a QR code - if yes, prepare to embed it
                has_qrcode = recipient_data.get('qrcode', '') != ''
                if has_qrcode:
                    # Replace {{qrcode}} placeholder with cid reference
                    temp_html = temp_html.replace("{{qrcode}}", "cid:qrcode")
                
                final_html_content = temp_html
                self.log_status(f"Preparing email content...")

                msg = MIMEMultipart('related')  # Changed to 'related' for inline images
                msg['From'] = self.smtp_email.get()
                msg['To'] = self.smtp_email.get()
                msg['Subject'] = subject
                msg['Reply-To'] = reply_to

                html_part = MIMEText(final_html_content, 'html')
                msg.attach(html_part)
                
                # Embed static images (uploaded via Upload Images button)
                for cid_name, image_path in self.embedded_images.items():
                    try:
                        with open(image_path, 'rb') as img_file:
                            img_data = img_file.read()
                            image = MIMEImage(img_data)
                            image.add_header('Content-ID', f'<{cid_name}>')
                            image.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
                            msg.attach(image)
                    except Exception as img_error:
                        self.log_status(f"⚠️ Could not embed {os.path.basename(image_path)}: {str(img_error)}")
                
                # Embed dynamic QR code for this specific recipient
                if has_qrcode:
                    qrcode_path = recipient_data['qrcode']
                    if os.path.exists(qrcode_path):
                        try:
                            with open(qrcode_path, 'rb') as qr_file:
                                qr_data = qr_file.read()
                                qr_image = MIMEImage(qr_data)
                                qr_image.add_header('Content-ID', '<qrcode>')
                                qr_image.add_header('Content-Disposition', 'inline', filename='qrcode.png')
                                msg.attach(qr_image)
                        except Exception as qr_error:
                            self.log_status(f"⚠️ Could not embed QR code for {recipient_data.get('email')}: {str(qr_error)}")
                    else:
                        self.log_status(f"⚠️ QR code file not found: {qrcode_path}")

                # الإرسال الفعلي، حيث يتم تمرير 'batch' كقائمة مستلمين، وهي تعمل كـ BCC
                server.sendmail(
                    from_addr=self.smtp_email.get(),
                    to_addrs=batch,
                    msg=msg.as_string()
                )

                total_sent += len(batch)
                self.log_status(f"✅ Batch {batch_idx + 1} sent successfully. ({total_sent} total emails)")

                progress = ((batch_idx + 1) / total_batches) * 100
                self.progress_var.set(progress)

                if batch_idx < total_batches - 1:
                    sleep_time = delay + random.uniform(0, 1)
                    self.log_status(f"😴 Waiting for {sleep_time:.1f} seconds before next batch...")
                    time.sleep(sleep_time)

            server.quit()

            self.log_status("\n" + "="*50)
            self.log_status(f"📊 Campaign completed!")
            self.log_status(f"✅ Successful: {total_sent}")
            self.log_status(f"Total Sent: {total_sent} (in {total_batches} batches)")

            messagebox.showinfo("Complete",
                                 f"Campaign finished!\n✅ Sent: {total_sent} recipients in {total_batches} batches.")

        except Exception as e:
            self.log_status(f"❌ Fatal error during campaign: {str(e)}")
            messagebox.showerror("Error", f"❌ Campaign failed: {str(e)}")

        finally:
            if server:
                try:
                    server.quit()
                except:
                    pass
            self.send_button.config(state="normal")
            self.progress_var.set(0)


    def load_smtp_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_smtp_config(self):
        config = {
            "server": self.smtp_server.get(),
            "port": self.smtp_port.get(),
            "email": self.smtp_email.get(),
            "reply_to": self.reply_to_email.get(),
            "password": self.smtp_password.get(),
            "delay": self.email_delay.get()
        }

        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Success", "✅ SMTP configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to save configuration: {str(e)}")

    def test_smtp_connection(self):
        try:
            server = smtplib.SMTP(self.smtp_server.get(), int(self.smtp_port.get()))
            server.starttls()
            server.login(self.smtp_email.get(), self.smtp_password.get())
            server.quit()
            messagebox.showinfo("Success", "✅ SMTP connection successful!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Connection failed: {str(e)}")

    def load_html_template(self):
        filename = filedialog.askopenfilename(
            title="Select HTML Template",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.html_editor.delete("1.0", tk.END)
                    self.html_editor.insert("1.0", f.read())
                messagebox.showinfo("Success", "✅ Template loaded successfully!")
                self.update_text_preview()
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to load template: {str(e)}")

    def import_recipients(self, file_type):
        if file_type == "csv":
            filename = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if row:
                                self.recipients_text.insert(tk.END, ','.join(row) + '\n')
                    messagebox.showinfo("Success", "✅ Recipients imported successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Failed to import: {str(e)}")

        elif file_type == "txt":
            filename = filedialog.askopenfilename(
                title="Select TXT File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        self.recipients_text.insert(tk.END, f.read())
                    messagebox.showinfo("Success", "✅ Recipients imported successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Failed to import: {str(e)}")

    def clear_recipients(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all recipients?"):
            self.recipients_text.delete("1.0", tk.END)

    def parse_recipients(self):
        recipients = []
        text = self.recipients_text.get("1.0", tk.END).strip()
        lines = text.split('\n')
        
        # Check if first line is a header
        first_line = lines[0].strip() if lines else ""
        has_header = 'email' in first_line.lower() or 'id' in first_line.lower()
        
        start_index = 1 if has_header else 0

        for line in lines[start_index:]:
            line = line.strip()
            if not line:
                continue

            if ',' in line:
                parts = [p.strip() for p in line.split(',')]
                
                # Support multiple formats:
                # Format 1: id,email,QRCode_Image,Name
                # Format 2: email,name,link
                # Format 3: email,name
                
                if len(parts) >= 4:
                    # Format: id,email,QRCode_Image,Name
                    email = parts[1]
                    qrcode_path = parts[2] if parts[2] else ""
                    name = parts[3] if parts[3] else ""
                    link = "#"
                elif len(parts) >= 3:
                    # Format: email,name,link OR email,QRCode,Name
                    email = parts[0]
                    # Check if second part looks like a file path
                    if os.path.exists(parts[1]) or '/' in parts[1] or '\\' in parts[1]:
                        qrcode_path = parts[1]
                        name = parts[2] if len(parts) > 2 else ""
                        link = "#"
                    else:
                        name = parts[1]
                        link = parts[2] if len(parts) > 2 else "#"
                        qrcode_path = ""
                elif len(parts) >= 2:
                    email = parts[0]
                    name = parts[1]
                    link = "#"
                    qrcode_path = ""
                else:
                    email = parts[0]
                    name = ""
                    link = "#"
                    qrcode_path = ""
            else:
                email = line.strip()
                name = ""
                link = "#"
                qrcode_path = ""

            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                recipients.append({
                    "email": email, 
                    "name": name if name else "Valued Customer", 
                    "link": link,
                    "qrcode": qrcode_path
                })

        return recipients

    def log_status(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()

def main():
    """Main application entry point"""
    root = tk.Tk()

    try:
        root.iconbitmap('email_icon.ico')
    except:
        pass

    root.update_idletasks()
    width = 1400
    height = 900
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.minsize(1100, 700)

    app = BulkEmailSender(root)
    def cleanup():
        if app.temp_html_file and os.path.exists(app.temp_html_file):
            try:
                os.remove(app.temp_html_file)
            except Exception as e:
                print(f"Could not clean up temp file: {e}")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", cleanup)

    root.mainloop()

if __name__ == "__main__":
    main()
