# 📱 QR Code Setup Guide

## Quick Start

### Step 1: Organize Your QR Codes

Put all your QR code images in this folder structure:

```
data/
└── qrcodes/
    ├── john_qr.png
    ├── jane_qr.png
    ├── bob_qr.png
    └── ... (your other QR codes)
```

**Supported formats:** PNG, JPG, JPEG, GIF, BMP

---

## Step 2: Create Your CSV File

Create a CSV file with this exact format:

```csv
id,email,QRCode_Image,Name
1,john@example.com,data/qrcodes/john_qr.png,John Doe
2,jane@example.com,data/qrcodes/jane_qr.png,Jane Smith
3,bob@example.com,data/qrcodes/bob_qr.png,Bob Johnson
```

**Important:**
- First line is the header (required)
- QRCode_Image path is relative to project root
- Use forward slashes (/) in paths
- Each row = one recipient with their unique QR code

---

## Step 3: Import in the App

1. Open the app and go to **👥 Recipients** tab
2. Click **"📂 Import CSV"** button
3. Select your CSV file
4. Recipients and their QR codes will be loaded

---

## Step 4: Add QR Code to Email Template

In the **✉️ Compose** tab, use the `{{qrcode}}` placeholder:

```html
<h1>Welcome {{name}}!</h1>
<p>Scan your personal QR code:</p>
<img src="cid:{{qrcode}}" alt="Your QR Code" />
```

The `{{qrcode}}` placeholder will be replaced with each recipient's QR code automatically!

---

## 📁 Helper Buttons in Recipients Tab

### 📱 Browse QR Codes
- Shows all QR codes in data/qrcodes/ folder
- Lists available QR code files
- Opens folder if no QR codes found

### 📁 Open QR Folder
- Opens data/qrcodes/ folder directly
- Drag and drop your QR codes here
- Organizes all QR codes in one place

### 📖 Show CSV Example
- Displays CSV format example
- Copy-paste template for your recipients
- Shows correct file paths

---

## 🎯 Complete Example

### Folder Structure
```
Email_sender/
├── data/
│   ├── qrcodes/           ← Put QR codes here
│   │   ├── john_qr.png
│   │   ├── jane_qr.png
│   │   └── bob_qr.png
│   └── recipients_with_qr.csv  ← Your recipients CSV
```

### CSV File (recipients_with_qr.csv)
```csv
id,email,QRCode_Image,Name
1,john@example.com,data/qrcodes/john_qr.png,John Doe
2,jane@example.com,data/qrcodes/jane_qr.png,Jane Smith
3,bob@example.com,data/qrcodes/bob_qr.png,Bob Johnson
```

### Email Template
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Hello {{name}}!</h1>
    
    <p>Welcome to our service! Here's your personal QR code:</p>
    
    <div style="text-align: center; margin: 20px;">
        <img src="cid:{{qrcode}}" alt="QR Code" style="width: 200px;" />
    </div>
    
    <p>Or visit your personal link: <a href="{{link}}">{{link}}</a></p>
</body>
</html>
```

---

## 💡 Tips & Best Practices

### ✅ DO:
- Keep QR codes in `data/qrcodes/` folder
- Use descriptive filenames (recipient_name_qr.png)
- Use relative paths in CSV: `data/qrcodes/filename.png`
- Test with 1-2 emails first
- Use PNG format for best quality

### ❌ DON'T:
- Don't use absolute paths (C:/Users/...)
- Don't use backslashes (\) - use forward slashes (/)
- Don't put QR codes outside the project folder
- Don't use spaces in filenames (use underscores)

---

## 🔧 Troubleshooting

### QR Code Not Showing?
1. Check file path is correct in CSV
2. Verify QR code file exists in data/qrcodes/
3. Use forward slashes: `data/qrcodes/file.png`
4. Check file extension matches actual file type

### CSV Import Error?
1. Make sure first line is header: `id,email,QRCode_Image,Name`
2. Check all rows have 4 columns
3. Use comma (,) as separator
4. Save as UTF-8 encoding

### Wrong QR Code Sent?
1. Verify each row in CSV has unique QR code path
2. Check QR code filename matches CSV entry
3. Test with small batch first

---

## 📊 CSV Formats Supported

### With QR Codes (Full Format)
```csv
id,email,QRCode_Image,Name
1,john@example.com,data/qrcodes/john.png,John Doe
```

### Without QR Codes (Simple Format)
```csv
email@example.com
email@example.com,Name
email@example.com,Name,https://link.com
```

The app auto-detects which format you're using!

---

## 🚀 Quick Commands in App

1. **Import CSV with QR codes:**
   - Recipients tab → Import CSV → Select your CSV

2. **Browse QR codes:**
   - Recipients tab → Browse QR Codes button

3. **Open QR folder:**
   - Recipients tab → Open QR Folder button

4. **See example:**
   - Recipients tab → Show CSV Example button

---

## 🎨 Sample QR Code Email

The default template in `templates/default_template.html` already includes QR code support:

```html
<div class="qr-section">
    <p>Or scan this QR code:</p>
    <img src="cid:{{qrcode}}" alt="QR Code" class="qr-code">
</div>
```

Just import your CSV and send!

---

**Need help? Check the Recipients tab for interactive buttons and guides!**
