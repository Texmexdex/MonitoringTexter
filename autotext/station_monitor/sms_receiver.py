"""
SMS Receiver - Poll for incoming messages from various providers
"""
import time
import threading
from typing import Callable, Optional
from database import Database
from message_parser import MessageParser

class SMSReceiver:
    """Base class for SMS receivers"""
    
    def __init__(self, config, db: Database, on_message_callback: Optional[Callable] = None):
        self.config = config
        self.db = db
        self.parser = MessageParser()
        self.on_message_callback = on_message_callback
        self.running = False
        self.thread = None
    
    def start(self):
        """Start receiving messages"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop receiving messages"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def _poll_loop(self):
        """Main polling loop - override in subclasses"""
        raise NotImplementedError
    
    def _process_message(self, phone_number: str, message_text: str):
        """Process an incoming message"""
        try:
            # Find station by phone number
            station = self.db.get_station_by_phone(phone_number)
            
            if not station:
                print(f"Unknown phone number: {phone_number}")
                return
            
            # Parse value from message
            value = self.parser.parse_value(message_text)
            
            if value is None:
                print(f"Could not parse value from: {message_text}")
                return
            
            # Save reading
            reading_id = self.db.add_reading(station['id'], value, message_text)
            
            print(f"Received reading from {station['name']}: {value}")
            
            # Callback for UI updates
            if self.on_message_callback:
                self.on_message_callback(station, value, message_text)
            
            # Check if alert and send notifications
            is_alert = value < station['min_value'] or value > station['max_value']
            if is_alert:
                self._send_alert_notifications(station, value)
        
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _send_alert_notifications(self, station, value):
        """Send alert notifications"""
        try:
            from notifications import NotificationManager
            from config import Config
            
            config = Config()
            notif_manager = NotificationManager(config)
            
            station_data = {
                'name': station['name'],
                'phone_number': station['phone_number'],
                'min_value': station['min_value'],
                'max_value': station['max_value'],
                'value': value
            }
            
            notif_manager.send_alert(station_data, value)
        except Exception as e:
            print(f"Error sending notifications: {e}")


class GoogleVoiceReceiver(SMSReceiver):
    """Receive SMS via Google Voice"""
    
    def __init__(self, config, db: Database, on_message_callback: Optional[Callable] = None):
        super().__init__(config, db, on_message_callback)
        self.voice = None
        self.processed_ids = set()
    
    def _poll_loop(self):
        """Poll Google Voice for new messages"""
        try:
            from googlevoice import Voice
        except ImportError:
            print("Google Voice library not installed. Run: pip install googlevoice")
            return
        
        gv_config = self.config.config.get("email", {})
        email = gv_config.get("email_address", "")
        password = gv_config.get("password", "")
        check_interval = gv_config.get("check_interval", 60)
        
        if not all([email, password]):
            print("Google Voice credentials not configured")
            return
        
        try:
            # Login
            self.voice = Voice()
            self.voice.login(email, password)
            print("Google Voice receiver started")
            
            while self.running:
                try:
                    # Fetch SMS messages
                    self.voice.sms()
                    
                    # Parse messages
                    for message in self.voice.sms.html.findAll('div', {'class': 'gc-message-sms-row'}):
                        msg_id = message.get('id')
                        
                        # Skip if already processed
                        if msg_id in self.processed_ids:
                            continue
                        
                        # Extract phone number and text
                        phone_span = message.find('span', {'class': 'gc-message-sms-from'})
                        text_span = message.find('span', {'class': 'gc-message-sms-text'})
                        
                        if phone_span and text_span:
                            phone_number = phone_span.text.strip()
                            message_text = text_span.text.strip()
                            
                            # Process message
                            self._process_message(phone_number, message_text)
                            
                            # Mark as processed
                            self.processed_ids.add(msg_id)
                    
                    # Wait before next check
                    time.sleep(check_interval)
                
                except Exception as e:
                    print(f"Error checking Google Voice: {e}")
                    time.sleep(check_interval)
        
        except Exception as e:
            print(f"Google Voice receiver error: {e}")


class EmailReceiver(SMSReceiver):
    """Receive SMS forwarded to email"""
    
    def _poll_loop(self):
        """Poll email for forwarded SMS"""
        import imaplib
        import email
        from email.header import decode_header
        
        email_config = self.config.config.get("email", {})
        imap_server = email_config.get("imap_server", "")
        imap_port = email_config.get("imap_port", 993)
        email_address = email_config.get("email_address", "")
        password = email_config.get("password", "")
        check_interval = email_config.get("check_interval", 60)
        
        if not all([imap_server, email_address, password]):
            print("Email credentials not configured")
            return
        
        print("Email receiver started")
        processed_uids = set()
        
        while self.running:
            try:
                # Connect to email
                mail = imaplib.IMAP4_SSL(imap_server, imap_port)
                mail.login(email_address, password)
                mail.select("INBOX")
                
                # Search for unread messages
                status, messages = mail.search(None, "UNSEEN")
                
                if status == "OK":
                    for num in messages[0].split():
                        if num in processed_uids:
                            continue
                        
                        # Fetch message
                        status, msg_data = mail.fetch(num, "(RFC822)")
                        
                        if status == "OK":
                            email_body = msg_data[0][1]
                            email_message = email.message_from_bytes(email_body)
                            
                            # Extract sender and body
                            from_header = email_message.get("From", "")
                            
                            # Get message body
                            body = ""
                            if email_message.is_multipart():
                                for part in email_message.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        break
                            else:
                                body = email_message.get_payload(decode=True).decode()
                            
                            # Try to extract phone number from sender or body
                            # This is provider-specific and may need customization
                            phone_number = self._extract_phone_from_email(from_header, body)
                            
                            if phone_number and body:
                                self._process_message(phone_number, body)
                            
                            processed_uids.add(num)
                
                mail.close()
                mail.logout()
                
                # Wait before next check
                time.sleep(check_interval)
            
            except Exception as e:
                print(f"Error checking email: {e}")
                time.sleep(check_interval)
    
    def _extract_phone_from_email(self, from_header: str, body: str) -> Optional[str]:
        """Extract phone number from email - customize based on your carrier"""
        import re
        
        # Try to find phone number in from header or body
        # Common formats: +1234567890, (123) 456-7890, 123-456-7890
        patterns = [
            r'\+\d{10,15}',
            r'\d{10}',
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\d{3}-\d{3}-\d{4}'
        ]
        
        text = from_header + " " + body
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                # Clean up and return
                phone = match.group()
                phone = re.sub(r'[^\d+]', '', phone)
                if not phone.startswith('+'):
                    phone = '+1' + phone  # Assume US if no country code
                return phone
        
        return None


class ReceiverManager:
    """Manage SMS receivers"""
    
    def __init__(self, config, db: Database):
        self.config = config
        self.db = db
        self.receiver = None
    
    def start(self, on_message_callback: Optional[Callable] = None):
        """Start appropriate receiver based on config"""
        self.stop()  # Stop any existing receiver
        
        sms_method = self.config.get_sms_method()
        
        if sms_method == "google_voice":
            self.receiver = GoogleVoiceReceiver(self.config, self.db, on_message_callback)
            self.receiver.start()
        elif sms_method == "email":
            self.receiver = EmailReceiver(self.config, self.db, on_message_callback)
            self.receiver.start()
        # Add other receivers as needed
    
    def stop(self):
        """Stop current receiver"""
        if self.receiver:
            self.receiver.stop()
            self.receiver = None
    
    def is_running(self) -> bool:
        """Check if receiver is running"""
        return self.receiver is not None and self.receiver.running
