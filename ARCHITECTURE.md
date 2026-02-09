# Project Architecture - Email Campaign Manager

## Application Flow

```
main.py (Entry Point)
    │
    └─> BulkEmailSender (Main Window)
            │
            ├─> ConfigManager (Configuration)
            │       └─> config/smtp_config.json
            │
            ├─> EmailSender (Business Logic)
            │       ├─> SMTP Connection
            │       ├─> Email Composition
            │       ├─> Recipient Parsing
            │       └─> Image/QR Embedding
            │
            ├─> AppStyles (UI Styling)
            │
            └─> UI Components
                    ├─> SMTPTab (Configure SMTP)
                    ├─> RecipientsTab (Manage Recipients)
                    ├─> ComposeTab (Compose Email)
                    ├─> SendTab (Send Campaign)
                    └─> ConnectionDialog (Connect Popup)
```

## Directory Structure

```
📁 Email_sender/
│
├── 📁 app/                          Main application package
│   ├── __init__.py                 Package initialization
│   ├── config.py                   ConfigManager class
│   ├── email_sender.py             EmailSender business logic
│   ├── html_parser.py              HTML parsing utilities
│   │
│   └── 📁 ui/                       User interface components
│       ├── __init__.py             UI package init
│       ├── main_window.py          Main application window
│       ├── tab_base.py             Base class for tabs
│       ├── styles.py               Centralized styling
│       ├── smtp_tab.py             SMTP configuration tab
│       ├── recipients_tab.py       Recipients management tab
│       ├── compose_tab.py          Email composition tab
│       ├── send_tab.py             Campaign sending tab
│       └── connection_dialog.py    Connection popup dialog
│
├── 📁 config/                       Configuration storage
│   └── smtp_config.json            SMTP credentials (auto-created)
│
├── 📁 data/                         Data files
│   ├── data.csv                    Sample recipient data
│   └── qrcodes/                    QR code images (user-created)
│
├── 📁 templates/                    Email HTML templates (optional)
│
├── main.py                          🎯 New entry point (run this!)
├── sender.py                        📜 Original monolithic version
├── README.md                        📖 Complete documentation
├── QUICKSTART.md                    ⚡ Quick start guide
├── requirement.txt                  📦 Dependencies info
└── .gitignore                       🔒 Git ignore rules
```

## Component Relationships

### ConfigManager (config.py)
- Loads/saves SMTP configuration from JSON
- Provides get/update/save methods
- Used by: All tabs, EmailSender

### EmailSender (email_sender.py)
- Handles SMTP connection and authentication
- Sends emails with HTML, images, QR codes
- Parses recipient CSV data
- Used by: SendTab, ConnectionDialog, SMTPTab

### HTMLTextExtractor (html_parser.py)
- Converts HTML to plain text for preview
- Used by: ComposeTab

### AppStyles (ui/styles.py)
- Defines color scheme and theme
- Configures TTK styles
- Used by: All UI components

### TabBase (ui/tab_base.py)
- Base class for all tabs
- Provides consistent header styling
- Inherited by: SMTPTab, RecipientsTab, ComposeTab, SendTab

### Main Window (ui/main_window.py)
- Creates main application window
- Manages top toolbar with connection status
- Creates all tabs
- Handles auto-connect on startup

### Tabs
- **SMTPTab**: Configure SMTP settings, save/test connection
- **RecipientsTab**: Import/manage recipients from CSV/TXT
- **ComposeTab**: Compose email with HTML, images, live preview
- **SendTab**: Send campaign with progress tracking

### Connection Dialog (ui/connection_dialog.py)
- Popup for SMTP authentication
- Tests connection and saves credentials
- Updates main window connection status

## Data Flow

### Sending Email Campaign

```
User Action (SendTab)
    │
    ├─> Get Subject (ComposeTab)
    ├─> Get Body (ComposeTab)
    ├─> Get Image (ComposeTab)
    └─> Get Recipients (RecipientsTab)
            ↓
    Parse Recipients (EmailSender)
    ├─> Detect CSV format (header/no header)
    ├─> Extract email, name, link, qrcode
    └─> Return list of recipients
            ↓
    For Each Recipient:
        ├─> Replace placeholders ({{name}}, {{link}})
        ├─> Embed image with CID reference
        ├─> Attach QR code if present
        ├─> Send via SMTP
        ├─> Update progress bar
        ├─> Log status
        └─> Delay before next email
            ↓
    Campaign Complete
```

### Configuration Flow

```
Application Start
    │
    └─> ConfigManager loads config/smtp_config.json
            ↓
    If credentials exist:
        ├─> Create EmailSender
        ├─> Test connection
        └─> Update UI (connected/not connected)
            ↓
    User clicks "Connect SMTP"
        ├─> Show ConnectionDialog
        ├─> Enter credentials
        ├─> Test connection
        ├─> Save to config/smtp_config.json
        └─> Update main window status
```

## Key Design Patterns

### Separation of Concerns
- **Business Logic**: `app/*.py` (no UI code)
- **UI Components**: `app/ui/*.py` (minimal business logic)
- **Configuration**: `config/` (persistent storage)

### Inheritance
- All tabs inherit from `TabBase` for consistent structure
- Provides reusable `create_header()` method

### Modular Architecture
- Each component has single responsibility
- Easy to maintain and extend
- Clear dependencies between modules

### MVC-inspired
- **Model**: ConfigManager, EmailSender (data and logic)
- **View**: All UI tabs (presentation)
- **Controller**: Main window coordinates interactions

## Extension Points

### Add New Tab
1. Create `app/ui/new_tab.py`
2. Inherit from `TabBase`
3. Implement `create_widgets()`
4. Import in `main_window.py`
5. Add to notebook

### Add Email Feature
1. Extend `EmailSender` class
2. Add method for new feature
3. Update `ComposeTab` or `SendTab` to use it

### Change Theme
1. Edit `AppStyles` in `app/ui/styles.py`
2. Update color constants
3. All tabs automatically use new colors

### Add Configuration Option
1. Add field to `SMTPTab`
2. Save via `ConfigManager`
3. Use in `EmailSender` or other component

## Performance Considerations

- **Email sending**: Done in background thread (SendTab)
- **Preview updates**: Debounced with 500ms delay
- **SMTP connection**: Reused across campaign (not per-email)
- **Large CSV files**: Parsed line-by-line (memory efficient)

## Security Notes

- SMTP passwords stored in plain text in `config/smtp_config.json`
- Recommended: Use app-specific passwords (e.g., Gmail App Passwords)
- `.gitignore` excludes config files from version control
- DO NOT commit `smtp_config.json` to public repositories

---

**This architecture provides a clean, maintainable, and extensible foundation for the Email Campaign Manager.**
