# 📱 QR Codes Folder

## Put Your QR Code Images Here!

This folder is for storing QR code images that will be attached to your emails.

### ✅ What to do:

1. **Copy your QR code images** to this folder
2. **Name them clearly** (e.g., `john_qr.png`, `jane_qr.png`)
3. **Reference them in CSV** using path: `data/qrcodes/your_file.png`

---

## 📋 Supported Image Formats

- ✅ PNG (recommended)
- ✅ JPG / JPEG
- ✅ GIF
- ✅ BMP

---

## 📝 Example CSV Format

```csv
id,email,QRCode_Image,Name
1,john@example.com,data/qrcodes/john_qr.png,John Doe
2,jane@example.com,data/qrcodes/jane_qr.png,Jane Smith
```

---

## 🎯 Quick Tips

- Use **descriptive filenames** for easy identification
- Keep **one QR code per recipient**
- **No spaces** in filenames (use underscore: `john_qr.png`)
- **PNG format** recommended for best quality

---

## 🚀 How to Use in App

1. Put QR codes in this folder
2. Create CSV with format above
3. Go to Recipients tab → Import CSV
4. Use `{{qrcode}}` placeholder in email template
5. Send campaign!

---

**Each recipient gets their own unique QR code automatically! 🎉**
