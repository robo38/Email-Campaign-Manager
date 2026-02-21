import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import csv
import os


class RecipientsTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent, style="Main.TFrame")
        self.create_widgets()
    
    def create_widgets(self):
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
        
        # Main card
        card = ttk.Frame(scrollable_frame, style="Card.TFrame")
        card.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header
        ttk.Label(card, text="👥 Recipients Management", 
                 style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Import buttons
        import_frame = ttk.Frame(card, style="Card.TFrame")
        import_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(import_frame, text="📂 Import CSV", command=lambda: self.import_file("csv"),
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)
        
        ttk.Button(import_frame, text="📄 Import TXT", command=lambda: self.import_file("txt"),
                   style="Accent.TButton").pack(side=tk.LEFT, padx=8)
        
        ttk.Button(import_frame, text="📱 Browse QR Codes", command=self.browse_qr_codes,
                   style="Success.TButton").pack(side=tk.LEFT, padx=8)
        
        ttk.Button(import_frame, text="🗑️ Clear", command=self.clear_recipients,
                   style="Warning.TButton").pack(side=tk.LEFT, padx=8)
        
        # Recipients list
        ttk.Label(card, text="Recipients List:", style="Subheader.TLabel").pack(anchor="w", pady=(20, 8))
        
        # Recipients text frame with better styling
        text_frame = ttk.Frame(card, style="Card.TFrame")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.recipients_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("JetBrains Mono", 10),
            bg="#1a1a3a",
            fg="#f8fafc",
            insertbackground="#6366f1",
            relief="flat",
            padx=18,
            pady=18,
            height=12,
            highlightthickness=2,
            highlightbackground="#252550",
            highlightcolor="#6366f1"
        )
        self.recipients_text.pack(fill=tk.BOTH, expand=True)
        
        # Info section with better card styling
        info_card = ttk.Frame(card, style="Card.TFrame")
        info_card.pack(fill=tk.X, pady=(20, 0))
        
        info_frame = ttk.Frame(info_card, style="Card.TFrame")
        info_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(info_frame, text="💡 Supported Formats:", 
                 foreground="#0ea5e9", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(5, 8))
        
        formats = [
            "   📧 email@example.com  (one per line)",
            "   📧 email@example.com,https://link.com,Full Name  (CSV with link)",
            "   📧 email@example.com,https://link.com  (CSV with link, no name)"
        ]
        
        for fmt in formats:
            ttk.Label(info_frame, text=fmt, foreground="#f59e0b", 
                     font=("JetBrains Mono", 9)).pack(anchor="w", pady=2)
        
        # QR Code section with enhanced styling
        qr_card = ttk.Frame(card, style="Card.TFrame")
        qr_card.pack(fill=tk.X, pady=(15, 0))
        
        qr_frame = ttk.Frame(qr_card, style="Card.TFrame")
        qr_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(qr_frame, text="� Link Setup:", 
                 foreground="#8b5cf6", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(5, 8))
        
        qr_steps = [
            "   1️⃣ Create CSV with format:",
            "      email,link,full name",
            "      john@email.com,https://example.com/u/1,John Doe",
            "      jane@email.com,https://example.com/u/2,Jane Smith",
            "   2️⃣ Use {{link}} placeholder in your email template",
            "   3️⃣ Use {{name}} placeholder for the recipient's name"
        ]
        
        for step in qr_steps:
            ttk.Label(qr_frame, text=step, foreground="#a78bfa", 
                     font=("JetBrains Mono", 9)).pack(anchor="w", pady=2)
        
        # Helper button
        helper_frame = ttk.Frame(qr_frame, style="Card.TFrame")
        helper_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(helper_frame, text="📖 Show CSV Example", command=self.show_csv_example,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=(20, 8))
        
        ttk.Button(helper_frame, text="📁 Open QR Folder", command=self.open_qr_folder,
                   style="Success.TButton").pack(side=tk.LEFT, padx=8)
    
    def import_file(self, file_type):
        """Import recipients from file"""
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
                    messagebox.showinfo("Success", "✅ Recipients imported!")
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
                    messagebox.showinfo("Success", "✅ Recipients imported!")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Failed to import: {str(e)}")
    
    def clear_recipients(self):
        """Clear all recipients"""
        if messagebox.askyesno("Confirm", "Clear all recipients?"):
            self.recipients_text.delete("1.0", tk.END)
    
    def get_recipients_text(self):
        """Get recipients text"""
        return self.recipients_text.get("1.0", tk.END)
    
    def browse_qr_codes(self):
        """Browse and list QR codes in data/qrcodes folder"""
        qr_folder = os.path.join("data", "qrcodes")
        
        if not os.path.exists(qr_folder):
            if messagebox.askyesno("Create Folder?", 
                                  "QR codes folder doesn't exist.\nCreate data/qrcodes/?"):
                try:
                    os.makedirs(qr_folder, exist_ok=True)
                    messagebox.showinfo("Success", f"✅ Created folder: {qr_folder}")
                    # Open the folder
                    os.startfile(os.path.abspath(qr_folder))
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Failed to create folder: {str(e)}")
            return
        
        # List QR code files
        try:
            files = [f for f in os.listdir(qr_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if not files:
                messagebox.showinfo("No QR Codes", 
                                   f"📁 No QR code images found in {qr_folder}\n\n" +
                                   "Add your QR code PNG/JPG files to this folder.")
                if messagebox.askyesno("Open Folder?", "Open the QR codes folder now?"):
                    os.startfile(os.path.abspath(qr_folder))
                return
            
            # Show list of QR codes
            qr_list = "\n".join([f"  📱 {f}" for f in sorted(files)])
            messagebox.showinfo("QR Codes Found", 
                               f"Found {len(files)} QR code(s) in {qr_folder}:\n\n{qr_list}\n\n" +
                               "💡 Use these filenames in your CSV:\n" +
                               f"data/qrcodes/[filename]")
            
            if messagebox.askyesno("Open Folder?", "Open the QR codes folder?"):
                os.startfile(os.path.abspath(qr_folder))
                
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error browsing QR codes: {str(e)}")
    
    def open_qr_folder(self):
        """Open the QR codes folder in file explorer"""
        qr_folder = os.path.join("data", "qrcodes")
        
        if not os.path.exists(qr_folder):
            if messagebox.askyesno("Create Folder?", 
                                  "QR codes folder doesn't exist.\nCreate data/qrcodes/?"):
                try:
                    os.makedirs(qr_folder, exist_ok=True)
                    messagebox.showinfo("Success", f"✅ Created folder: {qr_folder}")
                    os.startfile(os.path.abspath(qr_folder))
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Failed to create folder: {str(e)}")
        else:
            try:
                os.startfile(os.path.abspath(qr_folder))
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to open folder: {str(e)}")
    
    def show_csv_example(self):
        """Show CSV example in a popup window"""
        example_window = tk.Toplevel(self.frame)
        example_window.title("CSV Example with QR Codes")
        example_window.geometry("700x500")
        example_window.configure(bg="#0f0f23")
        
        # Header
        header_frame = ttk.Frame(example_window, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Label(header_frame, text="📋 CSV Format Example", 
                 style="Header.TLabel").pack(anchor="w")
        
        # CSV Example
        csv_frame = ttk.Frame(example_window, style="Card.TFrame")
        csv_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        example_text = scrolledtext.ScrolledText(
            csv_frame,
            wrap=tk.WORD,
            font=("JetBrains Mono", 10),
            bg="#1a1a3a",
            fg="#f8fafc",
            relief="flat",
            padx=15,
            pady=15,
            highlightthickness=2,
            highlightbackground="#252550",
            highlightcolor="#6366f1"
        )
        example_text.pack(fill=tk.BOTH, expand=True)
        
        csv_content = """email,link,full name
john@example.com,https://example.com/update?id=1,John Doe
maria@example.com,https://example.com/update?id=2,Maria Garcia
ahmed@example.com,https://example.com/update?id=3,Ahmed Khan
sarah@example.com,https://example.com/update?id=4,Sarah Johnson

📝 Notes:
- First line is the header (column names)
- link column: the personalized URL for each recipient
- Use {{link}} in your email template to insert the link
- Use {{name}} in your email template to insert the name

💡 Without links (simpler format):
email
john@example.com
maria@example.com
ahmed@example.com

Or even simpler (plain text):
john@example.com
maria@example.com
ahmed@example.com"""

        example_text.insert("1.0", csv_content)
        example_text.config(state=tk.DISABLED)
        
        # Close button
        btn_frame = ttk.Frame(example_window, style="Card.TFrame")
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        ttk.Button(btn_frame, text="✅ Got it!", command=example_window.destroy,
                   style="Success.TButton").pack(side=tk.RIGHT)
