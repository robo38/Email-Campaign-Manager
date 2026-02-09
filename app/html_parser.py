"""
HTML Text Extraction Utility
"""
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    """Extract plain text from HTML content"""
    
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
