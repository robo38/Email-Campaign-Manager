# Quick Start Guide - Email Campaign Manager

## 🚀 Getting Started in 3 Steps

### Step 1: Run the Application

```bash
python main.py
```

Or use the original version:
```bash
python sender.py
```

### Step 2: Connect to SMTP

1. Click the **🔌 Connect SMTP** button in the top toolbar
2. Enter your email credentials:
   - **Gmail Users**:
     - Server: `smtp.gmail.com`
     - Port: `587`
     - Email: Your Gmail address
     - Password: [App Password](https://myaccount.google.com/apppasswords) (not your regular password)
   
   - **Outlook/Hotmail Users**:
     - Server: `smtp.office365.com`
     - Port: `587`
     
3. Click **Connect**
4. Credentials are saved automatically for next time!

### Step 3: Send Your Campaign

#### Add Recipients
- Go to **👥 Recipients** tab
- Import CSV/TXT file OR paste emails manually
- Formats supported:
  ```
  john@example.com
  john@example.com,John Doe
  john@example.com,John Doe,https://custom-link.com
  ```

#### Compose Email
- Go to **✉️ Compose** tab
- Enter subject (optional - auto-generated if empty)
- Write HTML email content
- Use placeholders: `{{name}}`, `{{link}}`, `{{qrcode}}`
- Upload image if needed
- Preview updates in real-time!

#### Send Campaign
- Go to **🚀 Send** tab
- Review campaign summary
- Click **Start Campaign**
- Monitor progress with real-time status log

---

## 📊 CSV Format for QR Codes

**Step 1: Prepare QR Codes**
- Put your QR code images in `data/qrcodes/` folder
- Click **"📁 Open QR Folder"** button in Recipients tab

**Step 2: Create CSV**
Create a CSV file with this structure:

```csv
id,email,QRCode_Image,Name
1,john@example.com,data/qrcodes/john_qr.png,John Doe
2,jane@example.com,data/qrcodes/jane_qr.png,Jane Smith
3,bob@example.com,data/qrcodes/bob_qr.png,Bob Johnson
```

**Step 3: Import & Send**
- Import CSV in Recipients tab
- Use `{{qrcode}}` placeholder in email template
- Each recipient gets their own QR code!

**Helper Buttons in Recipients Tab:**
- 📱 **Browse QR Codes** - See available QR codes
- 📁 **Open QR Folder** - Add QR code images
- 📖 **Show CSV Example** - Get copy-paste template

**Note**: Header row is optional - the app auto-detects it!

📚 **Detailed Guide:** See [data/QR_CODE_GUIDE.md](data/QR_CODE_GUIDE.md)

---

## 💡 Pro Tips

### Gmail App Password
1. Enable 2-Factor Authentication in Google Account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate App Password for "Mail"
4. Use this password (not your regular password) in SMTP settings

### Email Placeholders
- `{{name}}` - Replaced with recipient name from CSV
- `{{link}}` - Replaced with custom link per recipient
- `{{qrcode}}` - Embeds QR code image inline

### Design Templates
- Use [Beefree](https://beefree.io/) to design beautiful HTML emails
- Export as HTML and paste into Compose tab
- Images can be embedded directly (no external hosting needed)

### Troubleshooting

**Connection Failed?**
- Verify SMTP settings (server, port, email, password)
- Gmail: Use App Password, not regular password
- Check firewall/antivirus settings

**Emails Not Sending?**
- Ensure connection is established (green dot indicator)
- Verify recipients format is correct
- Check email content is not empty
- Check provider's sending limits (Gmail: ~500/day)

**QR Codes Not Working?**
- Verify file paths are correct (relative to project root)
- Check file exists and is readable
- Supported: PNG, JPG, JPEG, GIF, BMP

---

## 📁 Folder Structure

```
Email_sender/
├── app/                      # Application source code
│   ├── config.py            # Configuration management
│   ├── email_sender.py      # Email sending logic
│   ├── html_parser.py       # HTML parsing
│   └── ui/                  # UI components
│       ├── smtp_tab.py      # SMTP settings tab
│       ├── recipients_tab.py # Recipients management
│       ├── compose_tab.py   # Email composition
│       ├── send_tab.py      # Campaign sending
│       ├── connection_dialog.py
│       ├── main_window.py   # Main application
│       ├── styles.py        # UI styling
│       └── tab_base.py      # Base tab class
│
├── config/                  # Configuration storage
│   └── smtp_config.json    # SMTP credentials (auto-created)
│
├── data/                    # Data files
│   └── data.csv            # Sample recipient data
│
├── templates/               # Email templates
│
├── main.py                  # Application entry point
├── sender.py               # Original version
├── README.md               # Full documentation
└── requirement.txt         # Dependencies info
```

---

## 🎨 Modern Features

✅ **Ultra-Modern Dark UI** - Vibrant accents, smooth animations  
✅ **Persistent Login** - Auto-reconnect on startup  
✅ **Live Preview** - Real-time email preview before sending  
✅ **Image Embedding** - No external hosting needed  
✅ **QR Code Support** - Dynamic attachment per recipient  
✅ **Progress Tracking** - Real-time status log with timestamps  
✅ **Default Subject** - Auto-generated if empty  
✅ **Modular Code** - Clean, maintainable architecture  

---

## 🔧 Development

### Adding New Features
1. Edit `app/email_sender.py` for email logic
2. Edit `app/ui/*.py` for UI changes
3. Edit `app/ui/styles.py` for styling

### Creating New Tab
1. Create file in `app/ui/`
2. Inherit from `TabBase`
3. Implement `create_widgets()` method
4. Import and add to `main_window.py`

---

## 📧 Contact & Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review code comments for implementation details
3. Modify as needed for your use case

---

**Enjoy sending beautiful email campaigns! 🚀**
