# Email Campaign Manager

A modern, feature-rich bulk email campaign management application built with Python and Tkinter.

## 🎯 Quick Start

```bash
python main.py          # New modular version (recommended)
# OR
python sender.py        # Original version (still works!)
```

## Features

- ✉️ **Professional Email Sending** - Send personalized HTML emails with embedded images and QR codes
- 🎨 **Ultra-Modern UI** - Dark theme with vibrant accents and smooth animations
- 📊 **Campaign Management** - Import recipients from CSV/TXT, track sending progress
- 🔒 **Persistent Login** - Save SMTP credentials securely for quick reconnection
- 👁️ **Live Preview** - Real-time preview of email content before sending
- 🖼️ **Image Attachments** - Upload and embed images directly in emails
- 📱 **QR Code Support** - Dynamically attach QR codes per recipient from CSV
- ⚙️ **Flexible Configuration** - Easy SMTP server configuration with test connection
- 📄 **Default Template** - Professional HTML email template with CSS included
- 📁 **Organized Structure** - Clean folder organization for config, data, and templates

## Folder Structure

```
Email_sender/
│
├── app/                             # Application source code
│   ├── config.py                   # ConfigManager for SMTP settings
│   ├── email_sender.py             # EmailSender business logic
│   ├── html_parser.py              # HTMLTextExtractor for preview
│   │
│   └── ui/                         # UI components
│       ├── styles.py               # Centralized styling
│       ├── tab_base.py             # Reusable tab structure
│       ├── main_window.py          # Main app window
│       ├── smtp_tab.py             # SMTP configuration tab
│       ├── recipients_tab.py       # Recipients management
│       ├── compose_tab.py          # Email composition
│       ├── send_tab.py             # Campaign sending
│       └── connection_dialog.py    # Connection popup
│
├── config/                          # ⭐ Configuration files
│   └── smtp_config.json            # SMTP credentials (auto-created)
│
├── data/                            # ⭐ Data files
│   ├── data.csv                    # Sample recipient data
│   └── sample_with_qr.csv          # Sample with QR codes
│
├── templates/                       # ⭐ Email templates
│   ├── default_template.html       # Professional HTML template
│   └── styles.css                  # Email styling (auto-loaded)
│
├── main.py                          # 🎯 NEW entry point
├── sender.py                        # Legacy version (still works)
├── README.md                        # This file
├── QUICKSTART.md                    # Quick start guide  
├── ORGANIZATION.md                  # File organization guide
└── ARCHITECTURE.md                  # Architecture docs
```

**NEW:** All files are now properly organized:
- **config/** - SMTP settings and configuration
- **data/** - CSV files and QR code images  
- **templates/** - HTML email templates with CSS

See [ORGANIZATION.md](ORGANIZATION.md) for detailed file organization guide.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install required packages:

```bash
pip install -r requirement.txt
```

Note: `tkinter` is included with most Python installations. If you encounter issues, install it via:
- **Windows**: Included by default
- **macOS**: Included by default
- **Linux**: `sudo apt-get install python3-tk`

## Usage

### Starting the Application

Run the main entry point:

```bash
python main.py
```

Or run the original sender (if preferred):

```bash
python sender.py
```

### Configuration Steps

1. **Connect to SMTP Server**
   - Click the "🔌 Connect SMTP" button in the top toolbar
   - Enter your email server credentials:
     - Server: smtp.gmail.com (for Gmail)
     - Port: 587 (TLS) or 465 (SSL)
     - Email: your email address
     - Password: your app password
   - Click "Connect" to establish connection
   - Credentials are saved for future sessions

2. **Add Recipients**
   - Go to "👥 Recipients" tab
   - Import from CSV/TXT or enter manually
   - Supported formats:
     ```
     email@example.com
     email@example.com,John Doe
     email@example.com,John Doe,https://link.com
     id,email,QRCode_Image,Name    # CSV with QR codes
     ```

3. **Compose Email**
   - Go to "✉️ Compose" tab
   - **Default template auto-loads** with professional design
   - Click "📄 Load Template" to reload default template
   - Enter subject line (optional - auto-generated if empty)
   - Write or edit HTML email content
   - Use placeholders: `{{name}}`, `{{link}}`, `{{qrcode}}`
   - Upload image attachment if needed
   - Preview updates in real-time
   - Customize `templates/default_template.html` for your brand

4. **Send Campaign**
   - Go to "🚀 Send" tab
   - Review campaign summary
   - Click "Start Campaign" to begin sending
   - Monitor progress in real-time status log

### CSV Format for QR Codes

```csv
id,email,QRCode_Image,Name
1,john@example.com,qrcodes/john_qr.png,John Doe
2,jane@example.com,qrcodes/jane_qr.png,Jane Smith
```

- Header row is optional (auto-detected)
- QRCode_Image: path to QR code image file
- Images are dynamically attached per recipient

## SMTP Configuration

### Gmail Setup

1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the App Password in the SMTP settings

### Other Providers

- **Outlook/Hotmail**: smtp.office365.com, Port 587
- **Yahoo**: smtp.mail.yahoo.com, Port 587
- **Custom**: Contact your email provider for SMTP details

## Features Explained

### Persistent Login
- SMTP credentials saved in `config/smtp_config.json`
- Auto-connect on application startup
- Connection status displayed in top toolbar

### Email Placeholders
- `{{name}}` - Replaced with recipient name
- `{{link}}` - Replaced with custom link per recipient
- `{{qrcode}}` - Replaced with attached QR code image

### Image Embedding
- Images embedded using CID (Content-ID) references
- No external hosting required
- All images sent with email

### Default Subject
- If subject is empty, auto-generates: "Campaign - YYYY-MM-DD"
- Prevents sending errors

## Troubleshooting

### Connection Failed
- Check SMTP server and port settings
- Verify email and password are correct
- For Gmail: Use App Password, not regular password
- Check firewall/antivirus settings

### Emails Not Sending
- Ensure SMTP connection is established (green dot indicator)
- Check recipient format is valid
- Verify email content is not empty
- Check SMTP provider's sending limits

### QR Codes Not Attaching
- Ensure QR code image paths are correct
- Check file exists and is readable
- Supported formats: PNG, JPG, JPEG, GIF, BMP

## Development

### Code Structure

- **Business Logic**: `app/config.py`, `app/email_sender.py`, `app/html_parser.py`
- **UI Components**: `app/ui/*.py`
- **Styling**: `app/ui/styles.py` (centralized color scheme and TTK styles)
- **Tab System**: All tabs inherit from `TabBase` for consistency

### Extending Functionality

1. **Add New Tab**:
   - Create new file in `app/ui/` inheriting from `TabBase`
   - Implement `create_widgets()` method
   - Import and add to `main_window.py`

2. **Modify Styles**:
   - Edit `app/ui/styles.py`
   - Update color constants or TTK style configuration

3. **Add Email Features**:
   - Extend `EmailSender` class in `app/email_sender.py`
   - Update compose tab to support new features

## License

This project is provided as-is for educational and personal use.

## Credits

Built with Python, Tkinter, and ❤️

---

For issues or questions, check the code comments or modify as needed for your use case.
