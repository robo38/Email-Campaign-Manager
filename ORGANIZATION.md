# 📁 Project Organization - Clean Structure

## ✅ Final Directory Structure

```
Email_sender/
│
├── 📁 app/                          # Application source code
│   ├── __init__.py                 # Package initialization
│   ├── config.py                   # ConfigManager - SMTP settings
│   ├── email_sender.py             # EmailSender - business logic
│   ├── html_parser.py              # HTMLTextExtractor - parsing
│   │
│   └── 📁 ui/                       # UI components
│       ├── __init__.py             
│       ├── main_window.py          # Main application window
│       ├── tab_base.py             # Base class for tabs
│       ├── styles.py               # Centralized styling
│       ├── smtp_tab.py             # SMTP configuration
│       ├── recipients_tab.py       # Recipients management
│       ├── compose_tab.py          # Email composition
│       ├── send_tab.py             # Campaign sending
│       └── connection_dialog.py    # Connection popup
│
├── 📁 config/                       # ⭐ Configuration files
│   └── smtp_config.json            # SMTP credentials (auto-created)
│
├── 📁 data/                         # ⭐ Data files
│   ├── data.csv                    # Sample recipient data
│   └── sample_with_qr.csv          # Sample with QR codes
│
├── 📁 templates/                    # ⭐ Email templates
│   ├── default_template.html       # Default HTML email template
│   └── styles.css                  # Email styling
│
├── 📄 main.py                       # 🎯 NEW entry point (use this!)
├── 📄 sender.py                     # Legacy version (still works)
├── 📄 README.md                     # Complete documentation
├── 📄 QUICKSTART.md                 # Quick start guide
├── 📄 ARCHITECTURE.md               # Architecture docs
├── 📄 requirement.txt               # Dependencies info
└── 📄 .gitignore                    # Git ignore rules
```

## 🎯 Where Everything Goes

### 📁 **config/** - Configuration Files
**What to put here:**
- ✅ `smtp_config.json` - Auto-generated when you connect to SMTP
- Any other app configuration files

**What's stored:**
```json
{
    "server": "smtp.gmail.com",
    "port": "587",
    "email": "your-email@gmail.com",
    "password": "your-app-password",
    "reply_to": "optional-reply@email.com",
    "delay": "10"
}
```

### 📁 **data/** - All Data Files
**What to put here:**
- ✅ CSV files with recipients
- ✅ QR code images (in data/qrcodes/)
- ✅ Any other data files

**Example CSV formats:**
```csv
# Simple format
email@example.com
email@example.com,John Doe

# With links
email@example.com,John Doe,https://link.com

# With QR codes
id,email,QRCode_Image,Name
1,john@example.com,data/qrcodes/john_qr.png,John Doe
```

### 📁 **templates/** - HTML & CSS Templates
**What to put here:**
- ✅ HTML email templates
- ✅ CSS stylesheets for emails
- Any other design files

**Default template includes:**
- Responsive design
- Modern gradient header
- Call-to-action button
- QR code section
- Professional footer
- Inline CSS for email compatibility

**To use custom templates:**
1. Create your HTML file in `templates/`
2. Create matching CSS file
3. Click "📄 Load Template" in Compose tab
4. Or edit `default_template.html` directly

## 🚀 Running the Application

### New Modular Version (Recommended)
```bash
python main.py
```

### Legacy Version (Still works!)
```bash
python sender.py
```

## 📝 File Purposes

| File/Folder | Purpose |
|------------|---------|
| `app/config.py` | Manages SMTP configuration, loads/saves settings |
| `app/email_sender.py` | Handles email sending, SMTP connection, recipient parsing |
| `app/html_parser.py` | Converts HTML to text for preview |
| `app/ui/styles.py` | Centralized UI theme and colors |
| `app/ui/tab_base.py` | Base class for consistent tab structure |
| `app/ui/main_window.py` | Main application window with toolbar |
| `app/ui/smtp_tab.py` | SMTP settings configuration |
| `app/ui/recipients_tab.py` | Import and manage recipients |
| `app/ui/compose_tab.py` | Compose emails with live preview |
| `app/ui/send_tab.py` | Send campaigns with progress tracking |
| `app/ui/connection_dialog.py` | SMTP connection popup |
| `config/smtp_config.json` | Stored SMTP credentials |
| `data/*.csv` | Recipient lists and data files |
| `templates/*.html` | Email HTML templates |
| `templates/*.css` | Email CSS stylesheets |
| `main.py` | Application entry point (NEW) |
| `sender.py` | Original monolithic version (LEGACY) |

## 🎨 Default Template Features

The default email template (`templates/default_template.html`) includes:

✨ **Professional Design**
- Modern gradient header (purple/indigo)
- Clean, readable typography
- Responsive for mobile devices
- Browser-style preview

✨ **Dynamic Content**
- `{{name}}` - Recipient name placeholder
- `{{link}}` - Custom link placeholder
- `{{qrcode}}` - QR code image placeholder

✨ **Components**
- Welcome header
- Bullet list with emoji icons
- Call-to-action button
- QR code section
- Professional footer with legal text

✨ **Styling** (`templates/styles.css`)
- Inline CSS ready for email clients
- Gradient backgrounds
- Hover effects on buttons
- Mobile-responsive breakpoints

## 🔧 Customization

### Change Default Template
1. Edit `templates/default_template.html`
2. Edit `templates/styles.css`
3. Restart app or click "Load Template"

### Add New Template
1. Create new HTML file in `templates/`
2. Update `compose_tab.py` to load your template
3. Or manually paste HTML into compose tab

### Modify Theme/Colors
Edit `app/ui/styles.py`:
```python
class AppStyles:
    # Change these colors
    BG_DARK = "#0a0a1a"
    ACCENT_PRIMARY = "#6366f1"
    ACCENT_SUCCESS = "#10b981"
    # ... etc
```

## 📊 Data File Examples

### Simple Recipients (`data/data.csv`)
```csv
john@example.com,John Doe
jane@example.com,Jane Smith
bob@example.com,Bob Johnson
```

### With QR Codes (`data/sample_with_qr.csv`)
```csv
id,email,QRCode_Image,Name
1,john@example.com,data/qrcodes/john_qr.png,John Doe
2,jane@example.com,data/qrcodes/jane_qr.png,Jane Smith
```

### With Custom Links
```csv
john@example.com,John Doe,https://example.com/john
jane@example.com,Jane Smith,https://example.com/jane
```

## 🗑️ Removed Files

These files were removed during cleanup:
- ❌ `test.py` - Data analysis file (not needed for email app)

These files were moved to proper folders:
- ✅ `data.csv` → `data/data.csv`
- ✅ `sample_with_qr.csv` → `data/sample_with_qr.csv`
- ✅ `smtp_config.json` → `config/smtp_config.json`

## 🔒 Security

**Protected by .gitignore:**
- `config/smtp_config.json` - Contains passwords
- `__pycache__/` - Python cache files
- `.vscode/`, `.idea/` - IDE settings

⚠️ **Never commit sensitive data to Git!**

## 📚 Documentation Files

- `README.md` - Complete feature documentation
- `QUICKSTART.md` - Quick start guide for users
- `ARCHITECTURE.md` - Technical architecture docs
- `requirement.txt` - Installation and dependencies

---

**Everything is now properly organized for easy maintenance and scaling! 🎉**
