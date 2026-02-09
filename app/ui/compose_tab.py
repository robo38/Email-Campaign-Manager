"""
Compose Email Tab
"""
from tkinter import ttk, scrolledtext, filedialog, messagebox
import tkinter as tk
import os
from .tab_base import TabBase
from ..html_parser import HTMLTextExtractor


class ComposeTab(TabBase):
    """Email Composition Tab"""
    
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
        """Create compose widgets"""
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
            "✉️ Compose Email",
            "Create your email content with HTML support and image attachments",
            "#8b5cf6"
        )
        
        # Split view: left for compose, right for preview
        paned = ttk.PanedWindow(scrollable_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Left: Compose
        left_card = ttk.Frame(paned, style="Card.TFrame", padding=30)
        paned.add(left_card, weight=1)
        
        # Subject
        ttk.Label(left_card, text="Subject:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 8))
        self.subject_entry = ttk.Entry(left_card, font=("Segoe UI", 11))
        self.subject_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Email body
        ttk.Label(left_card, text="Email Content (HTML):", style="Subheader.TLabel").pack(anchor="w", pady=(10, 8))
        
        self.email_body = scrolledtext.ScrolledText(
            left_card,
            wrap=tk.WORD,
            font=("JetBrains Mono", 10),
            bg="#1a1a3a",
            fg="#f8fafc",
            insertbackground="#6366f1",
            relief="flat",
            padx=18,
            pady=18,
            height=18,
            highlightthickness=2,
            highlightbackground="#252550",
            highlightcolor="#6366f1"
        )
        self.email_body.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Bind text change to update preview
        self.email_body.bind("<KeyRelease>", lambda e: self.app.schedule_preview_update())
        
        # Buttons frame
        buttons_frame = ttk.Frame(left_card, style="Card.TFrame")
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Template button
        ttk.Button(buttons_frame, text="📄 Load Template", command=self.load_template,
                   style="Success.TButton").pack(side=tk.LEFT, padx=8)
        
        # Image attachment
        img_frame = ttk.Frame(left_card, style="Card.TFrame")
        img_frame.pack(fill=tk.X)
        
        ttk.Button(img_frame, text="📎 Upload Image", command=self.upload_image,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)
        
        ttk.Button(img_frame, text="🗑️ Clear Image", command=self.clear_image,
                   style="Warning.TButton").pack(side=tk.LEFT, padx=8)
        
        self.image_label = ttk.Label(img_frame, text="No image attached",
                                     foreground="#9ca3af", font=("Segoe UI", 9))
        self.image_label.pack(side=tk.LEFT, padx=15)
        
        # Info
        info_text = "💡 Placeholders: {{name}}, {{link}}, {{qrcode}}"
        ttk.Label(left_card, text=info_text, foreground="#0ea5e9", 
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(15, 0))
        
        # Right: Live Preview
        right_card = ttk.Frame(paned, style="Card.TFrame", padding=30)
        paned.add(right_card, weight=1)
        
        # Preview header
        preview_header = ttk.Frame(right_card, style="Card.TFrame")
        preview_header.pack(fill=tk.X, pady=(0, 15))
        
        # Browser window style dots
        dots_frame = ttk.Frame(preview_header, style="Card.TFrame")
        dots_frame.pack(side=tk.LEFT)
        
        for color in ["#ef4444", "#f59e0b", "#10b981"]:
            dot = tk.Canvas(dots_frame, width=12, height=12, bg="#0e0e22", 
                          highlightthickness=0, bd=0)
            dot.pack(side=tk.LEFT, padx=3)
            dot.create_oval(2, 2, 10, 10, fill=color, outline="")
        
        ttk.Label(preview_header, text="Live Preview",
                 foreground="#9ca3af", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=12)
        
        # Preview text with improved styling
        self.preview_text = scrolledtext.ScrolledText(
            right_card,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#1e293b",
            relief="flat",
            padx=25,
            pady=25,
            state="disabled",
            height=18,
            highlightthickness=2,
            highlightbackground="#252550",
            highlightcolor="#6366f1"
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Image storage
        self.attached_image = None
        
        # Auto-load default template
        self.load_template(show_message=False)
    
    def load_template(self, show_message=True):
        """Load default HTML template with inline CSS"""
        try:
            # Get template directory
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            template_dir = os.path.join(current_dir, "templates")
            html_path = os.path.join(template_dir, "default_template.html")
            css_path = os.path.join(template_dir, "styles.css")
            
            # Read HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Read CSS
            css_content = ""
            if os.path.exists(css_path):
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
            
            # Inline CSS into HTML (replace <link> tag with <style>)
            if css_content:
                html_content = html_content.replace(
                    '<link rel="stylesheet" href="styles.css">',
                    f'<style>\n{css_content}\n    </style>'
                )
            
            # Set content
            self.email_body.delete("1.0", tk.END)
            self.email_body.insert("1.0", html_content)
            
            # Update preview
            self.app.schedule_preview_update()
            
            if show_message:
                messagebox.showinfo("Success", "✅ Template loaded!")
        except Exception as e:
            if show_message:
                messagebox.showerror("Error", f"❌ Failed to load template:\n{str(e)}")
    
    def upload_image(self):
        """Upload image attachment"""
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if filename:
            self.attached_image = filename
            import os
            self.image_label.config(text=f"📷 {os.path.basename(filename)}", foreground="#10b981")
            messagebox.showinfo("Success", "✅ Image attached!")
    
    def clear_image(self):
        """Clear attached image"""
        self.attached_image = None
        self.image_label.config(text="No image attached", foreground="#9ca3af")
    
    def get_subject(self):
        """Get email subject"""
        return self.subject_entry.get()
    
    def get_body(self):
        """Get email body"""
        return self.email_body.get("1.0", tk.END)
    
    def get_image(self):
        """Get attached image"""
        return self.attached_image
    
    def update_preview(self):
        """Update preview pane"""
        html_content = self.get_body()
        
        # Convert HTML to plain text for preview
        parser = HTMLTextExtractor()
        try:
            parser.feed(html_content)
            plain_text = parser.get_text()
        except:
            plain_text = html_content
        
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", plain_text)
        self.preview_text.config(state="disabled")
