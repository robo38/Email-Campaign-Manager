"""
Send Campaign Tab
"""
from tkinter import ttk, scrolledtext, messagebox
import tkinter as tk
from datetime import datetime
import threading
import time
from .tab_base import TabBase
from ..email_sender import EmailSender


class SendTab(TabBase):
    """Send Campaign Tab"""
    
    def create_header_in_frame(self, parent, title, subtitle, accent_color="#6366f1"):
        """Create header in specific frame"""
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        # Accent line
        accent_line = tk.Frame(header_frame, bg=accent_color, height=3)
        accent_line.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        ttk.Label(header_frame, text=title, style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        
        # Subtitle
        ttk.Label(header_frame, text=subtitle, foreground="#94a3b8", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 20))
        
        return header_frame
    
    def create_widgets(self):
        """Create send tab widgets"""
        # Create scrollable container
        canvas = tk.Canvas(self.frame, highlightthickness=0, bg="#0f0f23")
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.create_header_in_frame(
            scrollable_frame,
            "🚀 Send Campaign",
            "Review and launch your email campaign",
            "#10b981"
        )
        
        card = ttk.Frame(scrollable_frame, style="Card.TFrame", padding=30)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Campaign summary
        summary_frame = ttk.Frame(card, style="Card.TFrame")
        summary_frame.pack(fill=tk.X, pady=(0, 30))
        
        ttk.Label(summary_frame, text="📊 Campaign Summary",
                 foreground="#10b981", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 15))
        
        self.summary_label = ttk.Label(summary_frame, text="Ready to send",
                                       foreground="#9ca3af", font=("Segoe UI", 11))
        self.summary_label.pack(anchor="w", padx=20)
        
        # Progress bar
        ttk.Label(card, text="Progress:", style="Subheader.TLabel").pack(anchor="w", pady=(20, 8))
        
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(
            card,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            style="Success.Horizontal.TProgressbar",
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 8))
        
        self.progress_label = ttk.Label(card, text="0 / 0 sent",
                                       foreground="#9ca3af", font=("Segoe UI", 10))
        self.progress_label.pack(anchor="w")
        
        # Status log with improved styling
        ttk.Label(card, text="Status Log:", style="Subheader.TLabel").pack(anchor="w", pady=(25, 8))
        
        self.status_text = scrolledtext.ScrolledText(
            card,
            wrap=tk.WORD,
            font=("JetBrains Mono", 9),
            bg="#1a1a3a",
            fg="#f8fafc",
            relief="flat",
            padx=18,
            pady=18,
            height=12,
            state="disabled",
            highlightthickness=2,
            highlightbackground="#252550",
            highlightcolor="#6366f1"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Send button
        self.send_button = ttk.Button(
            card,
            text="🚀 Start Campaign",
            command=self.start_campaign,
            style="Success.TButton"
        )
        self.send_button.pack(pady=(10, 0))
        
        self.is_sending = False
    
    def log_status(self, message):
        """Log message to status text"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
    
    def start_campaign(self):
        """Start sending campaign"""
        if self.is_sending:
            messagebox.showwarning("Warning", "Campaign already in progress!")
            return
        
        # Validate
        if not self.app.email_sender:
            messagebox.showerror("Error", "❌ Not connected to SMTP server!")
            return
        
        subject = self.app.compose_tab.get_subject()
        body = self.app.compose_tab.get_body()
        recipients_text = self.app.recipients_tab.get_recipients_text()
        
        if not subject and not body:
            messagebox.showerror("Error", "❌ Email content is empty!")
            return
        
        if not recipients_text.strip():
            messagebox.showerror("Error", "❌ No recipients added!")
            return
        
        # Parse recipients
        recipients = self.app.email_sender.parse_recipients(recipients_text)
        
        if not recipients:
            messagebox.showerror("Error", "❌ Invalid recipients format!")
            return
        
        # Confirm
        count = len(recipients)
        if not messagebox.askyesno("Confirm", f"Send {count} emails?"):
            return
        
        # Start sending in thread
        self.is_sending = True
        self.send_button.config(state="disabled")
        
        threading.Thread(
            target=self.send_emails_thread,
            args=(subject, body, recipients),
            daemon=True
        ).start()
    
    def send_emails_thread(self, subject, body, recipients):
        """Send emails in background thread"""
        total = len(recipients)
        success = 0
        failed = 0
        
        self.log_status(f"🚀 Starting campaign: {total} emails")
        
        for i, recipient in enumerate(recipients, 1):
            try:
                # Default subject if empty
                final_subject = subject if subject.strip() else f"Campaign - {datetime.now().strftime('%Y-%m-%d')}"
                
                # Replace placeholders in HTML content
                personalized_body = body
                personalized_body = personalized_body.replace('{{name}}', recipient['name'])
                personalized_body = personalized_body.replace('{{link}}', recipient['link'])
                personalized_body = personalized_body.replace('{{qrcode}}', 'qrcode')  # Replace with Content-ID
                
                # Handle embedded images
                embedded_images = None
                attached_image = self.app.compose_tab.get_image()
                if attached_image:
                    embedded_images = {'attached_image': attached_image}
                
                # Send email with correct parameter names
                self.app.email_sender.send_email(
                    to_email=recipient['email'],
                    subject=final_subject,
                    html_content=personalized_body,
                    embedded_images=embedded_images,
                    qrcode_path=recipient.get('qrcode')
                )
                
                success += 1
                self.log_status(f"✅ Sent to {recipient['email']}")
                
            except Exception as e:
                failed += 1
                self.log_status(f"❌ Failed {recipient['email']}: {str(e)}")
            
            # Update progress
            progress = int((i / total) * 100)
            self.progress_var.set(progress)
            self.progress_label.config(text=f"{i} / {total} sent")
            
            # Delay between emails
            if i < total:
                delay = int(self.app.config_manager.get("delay", "10"))
                time.sleep(delay)
        
        # Complete
        self.log_status(f"✅ Campaign complete: {success} sent, {failed} failed")
        self.is_sending = False
        self.send_button.config(state="normal")
        
        messagebox.showinfo("Complete", f"Campaign finished!\n✅ {success} sent\n❌ {failed} failed")
