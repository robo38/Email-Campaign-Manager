"""
Configuration Management
"""
import json
import os


class ConfigManager:
    """Manage SMTP configuration"""
    
    def __init__(self, config_file="config/smtp_config.json"):
        self.config_file = config_file
        self.config = self.load()
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save(self, config):
        """Save configuration to file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def update(self, key_or_dict, value=None):
        """Update configuration value(s)"""
        if isinstance(key_or_dict, dict):
            # Update multiple values from dictionary
            self.config.update(key_or_dict)
        else:
            # Update single key-value pair
            self.config[key_or_dict] = value
