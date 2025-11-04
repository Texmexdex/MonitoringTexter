import json
import os

class Config:
    """Manage application configuration"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            "sms_method": "manual",  # manual, twilio, email, webhook
            "twilio": {
                "account_sid": "",
                "auth_token": "",
                "phone_number": "",
                "enabled": False
            },
            "email": {
                "imap_server": "",
                "imap_port": 993,
                "email_address": "",
                "password": "",
                "enabled": False,
                "check_interval": 60  # seconds
            },
            "webhook": {
                "port": 5000,
                "enabled": False
            },
            "notifications": {
                "email": {
                    "enabled": False,
                    "smtp_server": "",
                    "smtp_port": 587,
                    "from_email": "",
                    "password": "",
                    "to_emails": []
                },
                "sms": {
                    "enabled": False,
                    "provider": "twilio",  # twilio, vonage, aws_sns, google_voice, webhook
                    "to_numbers": []
                },
                "push": {
                    "enabled": False,
                    "webhook_url": "",
                    "api_key": ""
                }
            },
            "sms_providers": {
                "twilio": {
                    "account_sid": "",
                    "auth_token": "",
                    "from_number": ""
                },
                "vonage": {
                    "api_key": "",
                    "api_secret": "",
                    "from_number": ""
                },
                "aws_sns": {
                    "access_key_id": "",
                    "secret_access_key": "",
                    "region": "us-east-1"
                },
                "google_voice": {
                    "email": "",
                    "password": ""
                },
                "webhook": {
                    "url": "",
                    "api_key": ""
                }
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    config = self.default_config.copy()
                    config.update(loaded)
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
    
    def get_sms_method(self):
        """Get current SMS reception method"""
        return self.config.get("sms_method", "manual")
    
    def set_sms_method(self, method):
        """Set SMS reception method"""
        if method in ["manual", "twilio", "email", "webhook"]:
            self.config["sms_method"] = method
            return True
        return False
