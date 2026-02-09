"""
Email Sending Logic
"""
import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import re


class EmailSender:
    """Handle email sending operations"""
    
    def __init__(self, server, port, email, password, reply_to=None):
        self.server_address = server
        self.port = port
        self.email = email
        self.password = password
        self.reply_to = reply_to or email
        self.server = None
    
    def connect(self):
        """Connect to SMTP server"""
        try:
            self.server = smtplib.SMTP(self.server_address, int(self.port))
            self.server.starttls()
            self.server.login(self.email, self.password)
            return True
        except Exception as e:
            raise Exception(f"Connection failed: {str(e)}")
    
    def disconnect(self):
        """Disconnect from SMTP server"""
        if self.server:
            try:
                self.server.quit()
            except:
                pass
            self.server = None
    
    def test_connection(self):
        """Test SMTP connection and keep it open"""
        try:
            self.server = smtplib.SMTP(self.server_address, int(self.port))
            self.server.starttls()
            self.server.login(self.email, self.password)
            return True
        except Exception as e:
            self.server = None
            raise Exception(f"Connection test failed: {str(e)}")
    
    def send_email(self, to_email, subject, html_content, embedded_images=None, qrcode_path=None):
        """Send a single email"""
        # Ensure connection is active
        if not self.server:
            self.connect()
        
        msg = MIMEMultipart('related')
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg['Reply-To'] = self.reply_to
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Embed static images
        if embedded_images:
            for cid_name, image_path in embedded_images.items():
                try:
                    with open(image_path, 'rb') as img_file:
                        img_data = img_file.read()
                        image = MIMEImage(img_data)
                        image.add_header('Content-ID', f'<{cid_name}>')
                        image.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
                        msg.attach(image)
                except Exception as img_error:
                    print(f"Could not embed {os.path.basename(image_path)}: {str(img_error)}")
        
        # Embed dynamic QR code
        if qrcode_path and os.path.exists(qrcode_path):
            try:
                with open(qrcode_path, 'rb') as qr_file:
                    qr_data = qr_file.read()
                    qr_image = MIMEImage(qr_data)
                    qr_image.add_header('Content-ID', '<qrcode>')
                    qr_image.add_header('Content-Disposition', 'inline', filename='qrcode.png')
                    msg.attach(qr_image)
            except Exception as qr_error:
                print(f"Could not embed QR code: {str(qr_error)}")
        
        try:
            self.server.sendmail(self.email, to_email, msg.as_string())
        except (smtplib.SMTPServerDisconnected, AttributeError):
            # Reconnect if connection was lost
            self.connect()
            self.server.sendmail(self.email, to_email, msg.as_string())
    
    @staticmethod
    def remove_beefree_watermark(html_content):
        """Remove Beefree watermark from HTML"""
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
    
    @staticmethod
    def parse_recipients(text):
        """Parse recipients from text"""
        recipients = []
        lines = text.strip().split('\n')
        
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
                
                if len(parts) >= 4:
                    # Format: id,email,QRCode_Image,Name
                    email = parts[1]
                    qrcode_path = parts[2] if parts[2] else ""
                    name = parts[3] if parts[3] else ""
                    link = "#"
                elif len(parts) >= 3:
                    # Format: email,name,link OR email,QRCode,Name
                    email = parts[0]
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
