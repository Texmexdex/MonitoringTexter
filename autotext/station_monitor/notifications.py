import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import requests
import json

class NotificationManager:
    """Manage sending notifications via email, SMS, and push"""
    
    def __init__(self, config):
        self.config = config
    
    def send_alert(self, station_data: Dict, reading_value: float) -> Dict[str, bool]:
        """
        Send alert via all enabled notification methods
        Returns dict of {method: success}
        """
        results = {}
        
        notification_config = self.config.config.get("notifications", {})
        
        # Prepare alert message
        station_name = station_data.get('name', 'Unknown')
        phone = station_data.get('phone_number', '')
        min_val = station_data.get('min_value', 0)
        max_val = station_data.get('max_value', 0)
        
        subject = f"⚠️ Alert: {station_name} Out of Range"
        
        if reading_value < min_val:
            status = f"BELOW minimum ({reading_value:.2f} < {min_val:.1f})"
        else:
            status = f"ABOVE maximum ({reading_value:.2f} > {max_val:.1f})"
        
        message = f"""
Alert: {station_name}

Status: {status}
Current Value: {reading_value:.2f}
Safe Range: {min_val:.1f} - {max_val:.1f}
Station Phone: {phone}

Action Required: Contact technician to adjust readings.
"""
        
        # Send via enabled methods
        if notification_config.get("email", {}).get("enabled", False):
            results["email"] = self.send_email_notification(subject, message)
        
        if notification_config.get("sms", {}).get("enabled", False):
            results["sms"] = self.send_sms_notification(subject, message)
        
        if notification_config.get("push", {}).get("enabled", False):
            results["push"] = self.send_push_notification(subject, message, station_data)
        
        return results
    
    def send_email_notification(self, subject: str, message: str) -> bool:
        """Send email notification"""
        try:
            email_config = self.config.config.get("notifications", {}).get("email", {})
            
            smtp_server = email_config.get("smtp_server", "")
            smtp_port = email_config.get("smtp_port", 587)
            from_email = email_config.get("from_email", "")
            password = email_config.get("password", "")
            to_emails = email_config.get("to_emails", [])
            
            if not all([smtp_server, from_email, password, to_emails]):
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(from_email, password)
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"Email notification failed: {e}")
            return False
    
    def send_sms_notification(self, subject: str, message: str) -> bool:
        """Send SMS notification via configured provider"""
        try:
            sms_config = self.config.config.get("notifications", {}).get("sms", {})
            provider = sms_config.get("provider", "twilio")
            to_numbers = sms_config.get("to_numbers", [])
            
            if not to_numbers:
                return False
            
            # Combine subject and message for SMS
            sms_text = f"{subject}\n\n{message}"
            
            # Route to appropriate provider
            if provider == "twilio":
                return self._send_twilio_sms(sms_text, to_numbers)
            elif provider == "vonage":
                return self._send_vonage_sms(sms_text, to_numbers)
            elif provider == "aws_sns":
                return self._send_aws_sns_sms(sms_text, to_numbers)
            elif provider == "google_voice":
                return self._send_google_voice_sms(sms_text, to_numbers)
            elif provider == "webhook":
                return self._send_webhook_sms(sms_text, to_numbers)
            
            return False
        
        except Exception as e:
            print(f"SMS notification failed: {e}")
            return False
    
    def _send_twilio_sms(self, message: str, to_numbers: list) -> bool:
        """Send SMS via Twilio"""
        try:
            twilio_config = self.config.config.get("sms_providers", {}).get("twilio", {})
            account_sid = twilio_config.get("account_sid", "")
            auth_token = twilio_config.get("auth_token", "")
            from_number = twilio_config.get("from_number", "")
            
            if not all([account_sid, auth_token, from_number]):
                return False
            
            # Twilio REST API
            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            
            success_count = 0
            for to_number in to_numbers:
                try:
                    response = requests.post(
                        url,
                        auth=(account_sid, auth_token),
                        data={
                            "From": from_number,
                            "To": to_number,
                            "Body": message
                        },
                        timeout=10
                    )
                    if response.status_code == 201:
                        success_count += 1
                except Exception as e:
                    print(f"Failed to send to {to_number}: {e}")
            
            return success_count > 0
        
        except Exception as e:
            print(f"Twilio SMS failed: {e}")
            return False
    
    def _send_vonage_sms(self, message: str, to_numbers: list) -> bool:
        """Send SMS via Vonage (Nexmo)"""
        try:
            vonage_config = self.config.config.get("sms_providers", {}).get("vonage", {})
            api_key = vonage_config.get("api_key", "")
            api_secret = vonage_config.get("api_secret", "")
            from_number = vonage_config.get("from_number", "")
            
            if not all([api_key, api_secret, from_number]):
                return False
            
            # Vonage REST API
            url = "https://rest.nexmo.com/sms/json"
            
            success_count = 0
            for to_number in to_numbers:
                try:
                    response = requests.post(
                        url,
                        json={
                            "api_key": api_key,
                            "api_secret": api_secret,
                            "from": from_number,
                            "to": to_number,
                            "text": message
                        },
                        timeout=10
                    )
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("messages", [{}])[0].get("status") == "0":
                            success_count += 1
                except Exception as e:
                    print(f"Failed to send to {to_number}: {e}")
            
            return success_count > 0
        
        except Exception as e:
            print(f"Vonage SMS failed: {e}")
            return False
    
    def _send_aws_sns_sms(self, message: str, to_numbers: list) -> bool:
        """Send SMS via AWS SNS"""
        try:
            aws_config = self.config.config.get("sms_providers", {}).get("aws_sns", {})
            access_key = aws_config.get("access_key_id", "")
            secret_key = aws_config.get("secret_access_key", "")
            region = aws_config.get("region", "us-east-1")
            
            if not all([access_key, secret_key]):
                return False
            
            # Note: This requires boto3 library
            # For now, return False as it's not implemented
            print(f"AWS SNS SMS: Would send to {len(to_numbers)} numbers")
            return False
        
        except Exception as e:
            print(f"AWS SNS SMS failed: {e}")
            return False
    
    def _send_google_voice_sms(self, message: str, to_numbers: list) -> bool:
        """Send SMS via Google Voice"""
        try:
            gv_config = self.config.config.get("sms_providers", {}).get("google_voice", {})
            email = gv_config.get("email", "")
            password = gv_config.get("password", "")
            
            if not all([email, password]):
                return False
            
            try:
                from googlevoice import Voice
            except ImportError:
                print("Google Voice library not installed. Run: pip install googlevoice")
                return False
            
            # Login to Google Voice
            voice = Voice()
            voice.login(email, password)
            
            success_count = 0
            for to_number in to_numbers:
                try:
                    voice.send_sms(to_number, message)
                    success_count += 1
                except Exception as e:
                    print(f"Failed to send to {to_number}: {e}")
            
            return success_count > 0
        
        except Exception as e:
            print(f"Google Voice SMS failed: {e}")
            return False
    
    def _send_webhook_sms(self, message: str, to_numbers: list) -> bool:
        """Send SMS via custom webhook"""
        try:
            webhook_config = self.config.config.get("sms_providers", {}).get("webhook", {})
            url = webhook_config.get("url", "")
            api_key = webhook_config.get("api_key", "")
            
            if not url:
                return False
            
            headers = {
                "Content-Type": "application/json"
            }
            
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            payload = {
                "to_numbers": to_numbers,
                "message": message,
                "type": "alert"
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
        
        except Exception as e:
            print(f"Webhook SMS failed: {e}")
            return False
    
    def send_push_notification(self, subject: str, message: str, station_data: Dict) -> bool:
        """Send push notification to mobile app"""
        try:
            push_config = self.config.config.get("notifications", {}).get("push", {})
            
            webhook_url = push_config.get("webhook_url", "")
            api_key = push_config.get("api_key", "")
            
            if not webhook_url:
                return False
            
            # Prepare payload
            payload = {
                "title": subject,
                "message": message,
                "station": {
                    "name": station_data.get('name'),
                    "phone": station_data.get('phone_number'),
                    "value": station_data.get('value'),
                    "min": station_data.get('min_value'),
                    "max": station_data.get('max_value')
                },
                "priority": "high",
                "type": "alert"
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            # Send to webhook
            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
        
        except Exception as e:
            print(f"Push notification failed: {e}")
            return False
    
    def test_email(self) -> tuple[bool, str]:
        """Test email configuration"""
        try:
            email_config = self.config.config.get("notifications", {}).get("email", {})
            
            smtp_server = email_config.get("smtp_server", "")
            smtp_port = email_config.get("smtp_port", 587)
            from_email = email_config.get("from_email", "")
            password = email_config.get("password", "")
            to_emails = email_config.get("to_emails", [])
            
            if not all([smtp_server, from_email, password, to_emails]):
                return False, "Missing required configuration"
            
            # Test connection
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(from_email, password)
            
            # Send test email
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = "Test: Station Monitor Notification"
            
            test_message = "This is a test notification from Station Monitoring System.\n\nIf you received this, email notifications are working correctly!"
            msg.attach(MIMEText(test_message, 'plain'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(from_email, password)
                server.send_message(msg)
            
            return True, "Test email sent successfully!"
        
        except Exception as e:
            return False, f"Test failed: {str(e)}"
    
    def test_sms(self) -> tuple[bool, str]:
        """Test SMS configuration"""
        try:
            sms_config = self.config.config.get("notifications", {}).get("sms", {})
            
            if not sms_config.get("enabled", False):
                return False, "SMS notifications not enabled"
            
            # Twilio test would go here
            return False, "SMS testing not yet implemented"
        
        except Exception as e:
            return False, f"Test failed: {str(e)}"
    
    def test_push(self) -> tuple[bool, str]:
        """Test push notification configuration"""
        try:
            push_config = self.config.config.get("notifications", {}).get("push", {})
            
            webhook_url = push_config.get("webhook_url", "")
            api_key = push_config.get("api_key", "")
            
            if not webhook_url:
                return False, "Webhook URL not configured"
            
            # Send test notification
            payload = {
                "title": "Test Notification",
                "message": "This is a test from Station Monitoring System",
                "type": "test",
                "priority": "normal"
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Test notification sent successfully!"
            else:
                return False, f"Server returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            return False, "Request timed out"
        except requests.exceptions.ConnectionError:
            return False, "Could not connect to webhook URL"
        except Exception as e:
            return False, f"Test failed: {str(e)}"
