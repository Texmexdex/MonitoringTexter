import customtkinter as ctk
from tkinter import messagebox
from config import Config

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, db, config):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.db = db
        self.config = config
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Scrollable content
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.create_content()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")
        
        self.save_btn = ctk.CTkButton(
            header,
            text="💾 Save Settings",
            command=self.save_settings,
            width=120,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.save_btn.grid(row=0, column=1, padx=10)
    
    def create_content(self):
        # SMS Reception Method
        method_frame = ctk.CTkFrame(self.scroll_frame)
        method_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        method_frame.grid_columnconfigure(1, weight=1)
        
        # Header with status
        header_frame = ctk.CTkFrame(method_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(15, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="📱 SMS Reception Method",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        
        # Receiver status
        self.receiver_status_label = ctk.CTkLabel(
            header_frame,
            text="● Stopped",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.receiver_status_label.grid(row=0, column=1, padx=10)
        
        # Start/Stop button
        self.receiver_toggle_btn = ctk.CTkButton(
            header_frame,
            text="▶ Start Receiver",
            command=self.toggle_receiver,
            width=120,
            height=30
        )
        self.receiver_toggle_btn.grid(row=0, column=2)
        
        ctk.CTkLabel(
            method_frame,
            text="How do you want to receive text messages?",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 15))
        
        # Update receiver status
        self.update_receiver_status()
        
        self.method_var = ctk.StringVar(value=self.config.get_sms_method())
        
        methods = [
            ("manual", "Manual Entry", "Enter readings manually (current method)"),
            ("google_voice", "Google Voice", "Receive via Google Voice (FREE!)"),
            ("email", "Email Forwarding", "Forward texts to email (free)"),
            ("twilio", "Twilio SMS", "Receive SMS via Twilio API (~$1-2/month)"),
            ("webhook", "Webhook Receiver", "Receive via HTTP webhook (advanced)")
        ]
        
        for idx, (value, label, desc) in enumerate(methods):
            radio = ctk.CTkRadioButton(
                method_frame,
                text=label,
                variable=self.method_var,
                value=value,
                command=self.on_method_change,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            radio.grid(row=2+idx*2, column=0, sticky="w", padx=30, pady=(5, 2))
            
            ctk.CTkLabel(
                method_frame,
                text=desc,
                font=ctk.CTkFont(size=10),
                text_color="gray"
            ).grid(row=3+idx*2, column=0, sticky="w", padx=50, pady=(0, 10))
        
        # Twilio Settings
        self.twilio_frame = self.create_twilio_settings()
        self.twilio_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        # Email Settings
        self.email_frame = self.create_email_settings()
        self.email_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        # Webhook Settings
        self.webhook_frame = self.create_webhook_settings()
        self.webhook_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        
        # Notification Settings
        self.notification_frame = self.create_notification_settings()
        self.notification_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        
        # Update visibility
        self.on_method_change()
    
    def create_twilio_settings(self):
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame,
            text="📞 Twilio Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            frame,
            text="Sign up at twilio.com to get these credentials",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 15))
        
        # Account SID
        ctk.CTkLabel(frame, text="Account SID:", font=ctk.CTkFont(size=12)).grid(
            row=2, column=0, sticky="w", padx=15, pady=5
        )
        self.twilio_sid = ctk.CTkEntry(frame, placeholder_text="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.twilio_sid.grid(row=2, column=1, sticky="ew", padx=15, pady=5)
        self.twilio_sid.insert(0, self.config.config["twilio"]["account_sid"])
        
        # Auth Token
        ctk.CTkLabel(frame, text="Auth Token:", font=ctk.CTkFont(size=12)).grid(
            row=3, column=0, sticky="w", padx=15, pady=5
        )
        self.twilio_token = ctk.CTkEntry(frame, placeholder_text="Your auth token", show="*")
        self.twilio_token.grid(row=3, column=1, sticky="ew", padx=15, pady=5)
        self.twilio_token.insert(0, self.config.config["twilio"]["auth_token"])
        
        # Phone Number
        ctk.CTkLabel(frame, text="Twilio Phone:", font=ctk.CTkFont(size=12)).grid(
            row=4, column=0, sticky="w", padx=15, pady=5
        )
        self.twilio_phone = ctk.CTkEntry(frame, placeholder_text="+1234567890")
        self.twilio_phone.grid(row=4, column=1, sticky="ew", padx=15, pady=5)
        self.twilio_phone.insert(0, self.config.config["twilio"]["phone_number"])
        
        # Test button
        test_btn = ctk.CTkButton(
            frame,
            text="🧪 Test Connection",
            command=self.test_twilio,
            fg_color="gray",
            hover_color="#555"
        )
        test_btn.grid(row=5, column=0, columnspan=2, padx=15, pady=15)
        
        return frame
    
    def create_email_settings(self):
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame,
            text="📧 Email Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            frame,
            text="Forward texts to email, app will check inbox periodically",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 15))
        
        # IMAP Server
        ctk.CTkLabel(frame, text="IMAP Server:", font=ctk.CTkFont(size=12)).grid(
            row=2, column=0, sticky="w", padx=15, pady=5
        )
        self.email_server = ctk.CTkEntry(frame, placeholder_text="imap.gmail.com")
        self.email_server.grid(row=2, column=1, sticky="ew", padx=15, pady=5)
        self.email_server.insert(0, self.config.config["email"]["imap_server"])
        
        # Port
        ctk.CTkLabel(frame, text="Port:", font=ctk.CTkFont(size=12)).grid(
            row=3, column=0, sticky="w", padx=15, pady=5
        )
        self.email_port = ctk.CTkEntry(frame, placeholder_text="993")
        self.email_port.grid(row=3, column=1, sticky="ew", padx=15, pady=5)
        self.email_port.insert(0, str(self.config.config["email"]["imap_port"]))
        
        # Email Address
        ctk.CTkLabel(frame, text="Email Address:", font=ctk.CTkFont(size=12)).grid(
            row=4, column=0, sticky="w", padx=15, pady=5
        )
        self.email_address = ctk.CTkEntry(frame, placeholder_text="your@email.com")
        self.email_address.grid(row=4, column=1, sticky="ew", padx=15, pady=5)
        self.email_address.insert(0, self.config.config["email"]["email_address"])
        
        # Password
        ctk.CTkLabel(frame, text="Password:", font=ctk.CTkFont(size=12)).grid(
            row=5, column=0, sticky="w", padx=15, pady=5
        )
        self.email_password = ctk.CTkEntry(frame, placeholder_text="App password", show="*")
        self.email_password.grid(row=5, column=1, sticky="ew", padx=15, pady=5)
        self.email_password.insert(0, self.config.config["email"]["password"])
        
        # Check Interval
        ctk.CTkLabel(frame, text="Check Every:", font=ctk.CTkFont(size=12)).grid(
            row=6, column=0, sticky="w", padx=15, pady=5
        )
        interval_frame = ctk.CTkFrame(frame, fg_color="transparent")
        interval_frame.grid(row=6, column=1, sticky="ew", padx=15, pady=5)
        self.email_interval = ctk.CTkEntry(interval_frame, width=80)
        self.email_interval.pack(side="left", padx=(0, 5))
        self.email_interval.insert(0, str(self.config.config["email"]["check_interval"]))
        ctk.CTkLabel(interval_frame, text="seconds").pack(side="left")
        
        # Test button
        test_btn = ctk.CTkButton(
            frame,
            text="🧪 Test Connection",
            command=self.test_email,
            fg_color="gray",
            hover_color="#555"
        )
        test_btn.grid(row=7, column=0, columnspan=2, padx=15, pady=15)
        
        return frame
    
    def create_webhook_settings(self):
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame,
            text="🔗 Webhook Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            frame,
            text="Receive messages via HTTP POST requests (for advanced integrations)",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 15))
        
        # Port
        ctk.CTkLabel(frame, text="Port:", font=ctk.CTkFont(size=12)).grid(
            row=2, column=0, sticky="w", padx=15, pady=5
        )
        self.webhook_port = ctk.CTkEntry(frame, placeholder_text="5000")
        self.webhook_port.grid(row=2, column=1, sticky="ew", padx=15, pady=5)
        self.webhook_port.insert(0, str(self.config.config["webhook"]["port"]))
        
        # Webhook URL display
        ctk.CTkLabel(frame, text="Webhook URL:", font=ctk.CTkFont(size=12)).grid(
            row=3, column=0, sticky="w", padx=15, pady=5
        )
        self.webhook_url = ctk.CTkLabel(
            frame,
            text=f"http://localhost:{self.config.config['webhook']['port']}/webhook",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.webhook_url.grid(row=3, column=1, sticky="w", padx=15, pady=5)
        
        # Info
        info = ctk.CTkLabel(
            frame,
            text="POST JSON: {\"phone\": \"+1234567890\", \"message\": \"Station 1 - 56.893\"}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info.grid(row=4, column=0, columnspan=2, sticky="w", padx=15, pady=(5, 15))
        
        return frame
    
    def create_notification_settings(self):
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame,
            text="🔔 Alert Notifications",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            frame,
            text="Get notified when readings go out of range",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 15))
        
        # Email Notifications
        self.notify_email_var = ctk.BooleanVar(
            value=self.config.config.get("notifications", {}).get("email", {}).get("enabled", False)
        )
        email_check = ctk.CTkCheckBox(
            frame,
            text="📧 Email Notifications",
            variable=self.notify_email_var,
            command=self.toggle_email_notifications,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        email_check.grid(row=2, column=0, columnspan=2, sticky="w", padx=15, pady=(5, 10))
        
        # Email notification settings
        self.email_notify_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.email_notify_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 10))
        self.email_notify_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.email_notify_frame, text="SMTP Server:", font=ctk.CTkFont(size=11)).grid(
            row=0, column=0, sticky="w", padx=5, pady=3
        )
        self.notify_smtp = ctk.CTkEntry(self.email_notify_frame, placeholder_text="smtp.gmail.com")
        self.notify_smtp.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        self.notify_smtp.insert(0, self.config.config.get("notifications", {}).get("email", {}).get("smtp_server", ""))
        
        ctk.CTkLabel(self.email_notify_frame, text="Port:", font=ctk.CTkFont(size=11)).grid(
            row=1, column=0, sticky="w", padx=5, pady=3
        )
        self.notify_smtp_port = ctk.CTkEntry(self.email_notify_frame, placeholder_text="587", width=100)
        self.notify_smtp_port.grid(row=1, column=1, sticky="w", padx=5, pady=3)
        self.notify_smtp_port.insert(0, str(self.config.config.get("notifications", {}).get("email", {}).get("smtp_port", 587)))
        
        ctk.CTkLabel(self.email_notify_frame, text="From Email:", font=ctk.CTkFont(size=11)).grid(
            row=2, column=0, sticky="w", padx=5, pady=3
        )
        self.notify_from_email = ctk.CTkEntry(self.email_notify_frame, placeholder_text="alerts@yourdomain.com")
        self.notify_from_email.grid(row=2, column=1, sticky="ew", padx=5, pady=3)
        self.notify_from_email.insert(0, self.config.config.get("notifications", {}).get("email", {}).get("from_email", ""))
        
        ctk.CTkLabel(self.email_notify_frame, text="Password:", font=ctk.CTkFont(size=11)).grid(
            row=3, column=0, sticky="w", padx=5, pady=3
        )
        self.notify_email_pass = ctk.CTkEntry(self.email_notify_frame, placeholder_text="App password", show="*")
        self.notify_email_pass.grid(row=3, column=1, sticky="ew", padx=5, pady=3)
        self.notify_email_pass.insert(0, self.config.config.get("notifications", {}).get("email", {}).get("password", ""))
        
        ctk.CTkLabel(self.email_notify_frame, text="To Emails:", font=ctk.CTkFont(size=11)).grid(
            row=4, column=0, sticky="w", padx=5, pady=3
        )
        self.notify_to_emails = ctk.CTkEntry(self.email_notify_frame, placeholder_text="email1@domain.com, email2@domain.com")
        self.notify_to_emails.grid(row=4, column=1, sticky="ew", padx=5, pady=3)
        to_emails = self.config.config.get("notifications", {}).get("email", {}).get("to_emails", [])
        self.notify_to_emails.insert(0, ", ".join(to_emails))
        
        test_email_btn = ctk.CTkButton(
            self.email_notify_frame,
            text="🧪 Test Email",
            command=self.test_email_notification,
            fg_color="gray",
            hover_color="#555",
            width=100
        )
        test_email_btn.grid(row=5, column=1, sticky="e", padx=5, pady=10)
        
        # SMS Notifications
        self.notify_sms_var = ctk.BooleanVar(
            value=self.config.config.get("notifications", {}).get("sms", {}).get("enabled", False)
        )
        sms_check = ctk.CTkCheckBox(
            frame,
            text="📱 SMS Notifications",
            variable=self.notify_sms_var,
            command=self.toggle_sms_notifications,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        sms_check.grid(row=4, column=0, columnspan=2, sticky="w", padx=15, pady=(5, 10))
        
        # SMS notification settings
        self.sms_notify_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.sms_notify_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 10))
        self.sms_notify_frame.grid_columnconfigure(1, weight=1)
        
        # Provider selection
        ctk.CTkLabel(self.sms_notify_frame, text="SMS Provider:", font=ctk.CTkFont(size=11)).grid(
            row=0, column=0, sticky="w", padx=5, pady=3
        )
        self.sms_provider_var = ctk.StringVar(
            value=self.config.config.get("notifications", {}).get("sms", {}).get("provider", "twilio")
        )
        self.sms_provider_menu = ctk.CTkOptionMenu(
            self.sms_notify_frame,
            variable=self.sms_provider_var,
            values=["twilio", "vonage", "aws_sns", "google_voice", "webhook"],
            command=self.on_sms_provider_change
        )
        self.sms_provider_menu.grid(row=0, column=1, sticky="w", padx=5, pady=3)
        
        # To Numbers
        ctk.CTkLabel(self.sms_notify_frame, text="To Numbers:", font=ctk.CTkFont(size=11)).grid(
            row=1, column=0, sticky="w", padx=5, pady=3
        )
        self.notify_to_numbers = ctk.CTkEntry(self.sms_notify_frame, placeholder_text="+1234567890, +0987654321")
        self.notify_to_numbers.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        to_numbers = self.config.config.get("notifications", {}).get("sms", {}).get("to_numbers", [])
        self.notify_to_numbers.insert(0, ", ".join(to_numbers))
        
        # Provider-specific settings frames
        self.create_sms_provider_frames()
        
        # Show appropriate provider settings
        self.on_sms_provider_change(self.sms_provider_var.get())
        
        # Push Notifications
        self.notify_push_var = ctk.BooleanVar(
            value=self.config.config.get("notifications", {}).get("push", {}).get("enabled", False)
        )
        push_check = ctk.CTkCheckBox(
            frame,
            text="📲 Push Notifications (Mobile App)",
            variable=self.notify_push_var,
            command=self.toggle_push_notifications,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        push_check.grid(row=6, column=0, columnspan=2, sticky="w", padx=15, pady=(5, 10))
        
        # Push notification settings
        self.push_notify_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.push_notify_frame.grid(row=7, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 10))
        self.push_notify_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.push_notify_frame, text="Webhook URL:", font=ctk.CTkFont(size=11)).grid(
            row=0, column=0, sticky="w", padx=5, pady=3
        )
        self.notify_push_url = ctk.CTkEntry(self.push_notify_frame, placeholder_text="https://your-app.com/api/notifications")
        self.notify_push_url.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        self.notify_push_url.insert(0, self.config.config.get("notifications", {}).get("push", {}).get("webhook_url", ""))
        
        ctk.CTkLabel(self.push_notify_frame, text="API Key:", font=ctk.CTkFont(size=11)).grid(
            row=1, column=0, sticky="w", padx=5, pady=3
        )
        self.notify_push_key = ctk.CTkEntry(self.push_notify_frame, placeholder_text="Optional API key", show="*")
        self.notify_push_key.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        self.notify_push_key.insert(0, self.config.config.get("notifications", {}).get("push", {}).get("api_key", ""))
        
        ctk.CTkLabel(
            self.push_notify_frame,
            text="Configure your iOS/Android app to receive notifications at this webhook",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=3)
        
        test_push_btn = ctk.CTkButton(
            self.push_notify_frame,
            text="🧪 Test Push",
            command=self.test_push_notification,
            fg_color="gray",
            hover_color="#555",
            width=100
        )
        test_push_btn.grid(row=3, column=1, sticky="e", padx=5, pady=10)
        
        # Update visibility
        self.toggle_email_notifications()
        self.toggle_sms_notifications()
        self.toggle_push_notifications()
        
        return frame
    
    def toggle_email_notifications(self):
        """Show/hide email notification settings"""
        if self.notify_email_var.get():
            self.email_notify_frame.grid()
        else:
            self.email_notify_frame.grid_remove()
    
    def toggle_sms_notifications(self):
        """Show/hide SMS notification settings"""
        if self.notify_sms_var.get():
            self.sms_notify_frame.grid()
        else:
            self.sms_notify_frame.grid_remove()
    
    def toggle_push_notifications(self):
        """Show/hide push notification settings"""
        if self.notify_push_var.get():
            self.push_notify_frame.grid()
        else:
            self.push_notify_frame.grid_remove()
    
    def create_sms_provider_frames(self):
        """Create configuration frames for each SMS provider"""
        # Twilio frame
        self.sms_twilio_frame = ctk.CTkFrame(self.sms_notify_frame, fg_color="transparent")
        self.sms_twilio_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.sms_twilio_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.sms_twilio_frame, text="Account SID:", font=ctk.CTkFont(size=10)).grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_twilio_sid = ctk.CTkEntry(self.sms_twilio_frame, placeholder_text="ACxxxxxxxx")
        self.sms_twilio_sid.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.sms_twilio_sid.insert(0, self.config.config.get("sms_providers", {}).get("twilio", {}).get("account_sid", ""))
        
        ctk.CTkLabel(self.sms_twilio_frame, text="Auth Token:", font=ctk.CTkFont(size=10)).grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_twilio_token = ctk.CTkEntry(self.sms_twilio_frame, placeholder_text="Token", show="*")
        self.sms_twilio_token.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.sms_twilio_token.insert(0, self.config.config.get("sms_providers", {}).get("twilio", {}).get("auth_token", ""))
        
        ctk.CTkLabel(self.sms_twilio_frame, text="From Number:", font=ctk.CTkFont(size=10)).grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_twilio_from = ctk.CTkEntry(self.sms_twilio_frame, placeholder_text="+1234567890")
        self.sms_twilio_from.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        self.sms_twilio_from.insert(0, self.config.config.get("sms_providers", {}).get("twilio", {}).get("from_number", ""))
        
        # Vonage frame
        self.sms_vonage_frame = ctk.CTkFrame(self.sms_notify_frame, fg_color="transparent")
        self.sms_vonage_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.sms_vonage_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.sms_vonage_frame, text="API Key:", font=ctk.CTkFont(size=10)).grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_vonage_key = ctk.CTkEntry(self.sms_vonage_frame, placeholder_text="Your API key")
        self.sms_vonage_key.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.sms_vonage_key.insert(0, self.config.config.get("sms_providers", {}).get("vonage", {}).get("api_key", ""))
        
        ctk.CTkLabel(self.sms_vonage_frame, text="API Secret:", font=ctk.CTkFont(size=10)).grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_vonage_secret = ctk.CTkEntry(self.sms_vonage_frame, placeholder_text="Secret", show="*")
        self.sms_vonage_secret.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.sms_vonage_secret.insert(0, self.config.config.get("sms_providers", {}).get("vonage", {}).get("api_secret", ""))
        
        ctk.CTkLabel(self.sms_vonage_frame, text="From Number:", font=ctk.CTkFont(size=10)).grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_vonage_from = ctk.CTkEntry(self.sms_vonage_frame, placeholder_text="+1234567890 or Brand Name")
        self.sms_vonage_from.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        self.sms_vonage_from.insert(0, self.config.config.get("sms_providers", {}).get("vonage", {}).get("from_number", ""))
        
        # AWS SNS frame
        self.sms_aws_frame = ctk.CTkFrame(self.sms_notify_frame, fg_color="transparent")
        self.sms_aws_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.sms_aws_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.sms_aws_frame, text="Access Key ID:", font=ctk.CTkFont(size=10)).grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_aws_key = ctk.CTkEntry(self.sms_aws_frame, placeholder_text="AKIAXXXXXXXX")
        self.sms_aws_key.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.sms_aws_key.insert(0, self.config.config.get("sms_providers", {}).get("aws_sns", {}).get("access_key_id", ""))
        
        ctk.CTkLabel(self.sms_aws_frame, text="Secret Key:", font=ctk.CTkFont(size=10)).grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_aws_secret = ctk.CTkEntry(self.sms_aws_frame, placeholder_text="Secret", show="*")
        self.sms_aws_secret.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.sms_aws_secret.insert(0, self.config.config.get("sms_providers", {}).get("aws_sns", {}).get("secret_access_key", ""))
        
        ctk.CTkLabel(self.sms_aws_frame, text="Region:", font=ctk.CTkFont(size=10)).grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_aws_region = ctk.CTkEntry(self.sms_aws_frame, placeholder_text="us-east-1")
        self.sms_aws_region.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        self.sms_aws_region.insert(0, self.config.config.get("sms_providers", {}).get("aws_sns", {}).get("region", "us-east-1"))
        
        ctk.CTkLabel(
            self.sms_aws_frame,
            text="Note: Requires boto3 library (pip install boto3)",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        # Google Voice frame
        self.sms_gv_frame = ctk.CTkFrame(self.sms_notify_frame, fg_color="transparent")
        self.sms_gv_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.sms_gv_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.sms_gv_frame, text="Google Email:", font=ctk.CTkFont(size=10)).grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_gv_email = ctk.CTkEntry(self.sms_gv_frame, placeholder_text="your@gmail.com")
        self.sms_gv_email.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.sms_gv_email.insert(0, self.config.config.get("sms_providers", {}).get("google_voice", {}).get("email", ""))
        
        ctk.CTkLabel(self.sms_gv_frame, text="Password:", font=ctk.CTkFont(size=10)).grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_gv_password = ctk.CTkEntry(self.sms_gv_frame, placeholder_text="App password", show="*")
        self.sms_gv_password.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.sms_gv_password.insert(0, self.config.config.get("sms_providers", {}).get("google_voice", {}).get("password", ""))
        
        ctk.CTkLabel(
            self.sms_gv_frame,
            text="FREE! Use your Google Voice account. Requires googlevoice library.",
            font=ctk.CTkFont(size=9),
            text_color="green"
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        ctk.CTkLabel(
            self.sms_gv_frame,
            text="Note: Requires googlevoice library (pip install googlevoice)",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        # Webhook frame
        self.sms_webhook_frame = ctk.CTkFrame(self.sms_notify_frame, fg_color="transparent")
        self.sms_webhook_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.sms_webhook_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.sms_webhook_frame, text="Webhook URL:", font=ctk.CTkFont(size=10)).grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_webhook_url = ctk.CTkEntry(self.sms_webhook_frame, placeholder_text="https://your-sms-gateway.com/send")
        self.sms_webhook_url.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.sms_webhook_url.insert(0, self.config.config.get("sms_providers", {}).get("webhook", {}).get("url", ""))
        
        ctk.CTkLabel(self.sms_webhook_frame, text="API Key:", font=ctk.CTkFont(size=10)).grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.sms_webhook_key = ctk.CTkEntry(self.sms_webhook_frame, placeholder_text="Optional", show="*")
        self.sms_webhook_key.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.sms_webhook_key.insert(0, self.config.config.get("sms_providers", {}).get("webhook", {}).get("api_key", ""))
        
        ctk.CTkLabel(
            self.sms_webhook_frame,
            text='POST JSON: {"to_numbers": [...], "message": "..."}',
            font=ctk.CTkFont(size=9),
            text_color="gray"
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
    
    def on_sms_provider_change(self, provider=None):
        """Show/hide SMS provider settings based on selection"""
        if provider is None:
            provider = self.sms_provider_var.get()
        
        # Hide all
        self.sms_twilio_frame.grid_remove()
        self.sms_vonage_frame.grid_remove()
        self.sms_aws_frame.grid_remove()
        self.sms_gv_frame.grid_remove()
        self.sms_webhook_frame.grid_remove()
        
        # Show selected
        if provider == "twilio":
            self.sms_twilio_frame.grid()
        elif provider == "vonage":
            self.sms_vonage_frame.grid()
        elif provider == "aws_sns":
            self.sms_aws_frame.grid()
        elif provider == "google_voice":
            self.sms_gv_frame.grid()
        elif provider == "webhook":
            self.sms_webhook_frame.grid()
    
    def test_email_notification(self):
        """Test email notification"""
        from notifications import NotificationManager
        notif_manager = NotificationManager(self.config)
        success, message = notif_manager.test_email()
        
        if success:
            messagebox.showinfo("Test Successful", message)
        else:
            messagebox.showerror("Test Failed", message)
    
    def test_push_notification(self):
        """Test push notification"""
        from notifications import NotificationManager
        notif_manager = NotificationManager(self.config)
        success, message = notif_manager.test_push()
        
        if success:
            messagebox.showinfo("Test Successful", message)
        else:
            messagebox.showerror("Test Failed", message)
    
    def on_method_change(self):
        """Show/hide settings based on selected method"""
        method = self.method_var.get()
        
        # Hide all
        self.twilio_frame.grid_remove()
        self.email_frame.grid_remove()
        self.webhook_frame.grid_remove()
        
        # Show relevant
        if method == "twilio":
            self.twilio_frame.grid()
        elif method == "email":
            self.email_frame.grid()
        elif method == "webhook":
            self.webhook_frame.grid()
    
    def test_twilio(self):
        """Test Twilio connection"""
        messagebox.showinfo(
            "Test Twilio",
            "Twilio integration coming soon!\n\n"
            "This will verify your credentials and send a test message."
        )
    
    def test_email(self):
        """Test email connection"""
        messagebox.showinfo(
            "Test Email",
            "Email integration coming soon!\n\n"
            "This will connect to your email and check for messages."
        )
    
    def save_settings(self):
        """Save all settings"""
        try:
            # Save SMS method
            self.config.set_sms_method(self.method_var.get())
            
            # Save Twilio settings
            self.config.config["twilio"]["account_sid"] = self.twilio_sid.get().strip()
            self.config.config["twilio"]["auth_token"] = self.twilio_token.get().strip()
            self.config.config["twilio"]["phone_number"] = self.twilio_phone.get().strip()
            self.config.config["twilio"]["enabled"] = self.method_var.get() == "twilio"
            
            # Save Email settings
            self.config.config["email"]["imap_server"] = self.email_server.get().strip()
            self.config.config["email"]["imap_port"] = int(self.email_port.get().strip() or 993)
            self.config.config["email"]["email_address"] = self.email_address.get().strip()
            self.config.config["email"]["password"] = self.email_password.get().strip()
            self.config.config["email"]["check_interval"] = int(self.email_interval.get().strip() or 60)
            self.config.config["email"]["enabled"] = self.method_var.get() == "email"
            
            # Save Webhook settings
            self.config.config["webhook"]["port"] = int(self.webhook_port.get().strip() or 5000)
            self.config.config["webhook"]["enabled"] = self.method_var.get() == "webhook"
            
            # Save Notification settings
            # Email notifications
            self.config.config["notifications"]["email"]["enabled"] = self.notify_email_var.get()
            self.config.config["notifications"]["email"]["smtp_server"] = self.notify_smtp.get().strip()
            self.config.config["notifications"]["email"]["smtp_port"] = int(self.notify_smtp_port.get().strip() or 587)
            self.config.config["notifications"]["email"]["from_email"] = self.notify_from_email.get().strip()
            self.config.config["notifications"]["email"]["password"] = self.notify_email_pass.get().strip()
            to_emails = [e.strip() for e in self.notify_to_emails.get().split(",") if e.strip()]
            self.config.config["notifications"]["email"]["to_emails"] = to_emails
            
            # SMS notifications
            self.config.config["notifications"]["sms"]["enabled"] = self.notify_sms_var.get()
            self.config.config["notifications"]["sms"]["provider"] = self.sms_provider_var.get()
            to_numbers = [n.strip() for n in self.notify_to_numbers.get().split(",") if n.strip()]
            self.config.config["notifications"]["sms"]["to_numbers"] = to_numbers
            
            # SMS Provider configurations
            # Twilio
            self.config.config["sms_providers"]["twilio"]["account_sid"] = self.sms_twilio_sid.get().strip()
            self.config.config["sms_providers"]["twilio"]["auth_token"] = self.sms_twilio_token.get().strip()
            self.config.config["sms_providers"]["twilio"]["from_number"] = self.sms_twilio_from.get().strip()
            
            # Vonage
            self.config.config["sms_providers"]["vonage"]["api_key"] = self.sms_vonage_key.get().strip()
            self.config.config["sms_providers"]["vonage"]["api_secret"] = self.sms_vonage_secret.get().strip()
            self.config.config["sms_providers"]["vonage"]["from_number"] = self.sms_vonage_from.get().strip()
            
            # AWS SNS
            self.config.config["sms_providers"]["aws_sns"]["access_key_id"] = self.sms_aws_key.get().strip()
            self.config.config["sms_providers"]["aws_sns"]["secret_access_key"] = self.sms_aws_secret.get().strip()
            self.config.config["sms_providers"]["aws_sns"]["region"] = self.sms_aws_region.get().strip()
            
            # Google Voice
            self.config.config["sms_providers"]["google_voice"]["email"] = self.sms_gv_email.get().strip()
            self.config.config["sms_providers"]["google_voice"]["password"] = self.sms_gv_password.get().strip()
            
            # Webhook
            self.config.config["sms_providers"]["webhook"]["url"] = self.sms_webhook_url.get().strip()
            self.config.config["sms_providers"]["webhook"]["api_key"] = self.sms_webhook_key.get().strip()
            
            # Push notifications
            self.config.config["notifications"]["push"]["enabled"] = self.notify_push_var.get()
            self.config.config["notifications"]["push"]["webhook_url"] = self.notify_push_url.get().strip()
            self.config.config["notifications"]["push"]["api_key"] = self.notify_push_key.get().strip()
            
            # Save to file
            if self.config.save_config():
                enabled_methods = []
                if self.notify_email_var.get():
                    enabled_methods.append("Email")
                if self.notify_sms_var.get():
                    enabled_methods.append("SMS")
                if self.notify_push_var.get():
                    enabled_methods.append("Push")
                
                notif_msg = ""
                if enabled_methods:
                    notif_msg = f"\n\nNotifications enabled: {', '.join(enabled_methods)}"
                
                messagebox.showinfo(
                    "Success",
                    f"Settings saved successfully!{notif_msg}\n\n"
                    "Alerts will now be sent when readings go out of range."
                )
            else:
                messagebox.showerror("Error", "Failed to save settings")
        
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def refresh(self):
        """Refresh settings from config"""
        self.method_var.set(self.config.get_sms_method())
        self.on_method_change()
        self.update_receiver_status()
    
    def update_receiver_status(self):
        """Update receiver status display"""
        try:
            # Get receiver manager from main window
            main_window = self.master.master.master  # Navigate up to MainWindow
            if hasattr(main_window, 'receiver_manager'):
                is_running = main_window.receiver_manager.is_running()
                
                if is_running:
                    self.receiver_status_label.configure(
                        text="● Running",
                        text_color="green"
                    )
                    self.receiver_toggle_btn.configure(text="⏸ Stop Receiver")
                else:
                    self.receiver_status_label.configure(
                        text="● Stopped",
                        text_color="gray"
                    )
                    self.receiver_toggle_btn.configure(text="▶ Start Receiver")
        except:
            pass
    
    def toggle_receiver(self):
        """Start or stop the SMS receiver"""
        try:
            # Get receiver manager from main window
            main_window = self.master.master.master
            if not hasattr(main_window, 'receiver_manager'):
                messagebox.showerror("Error", "Receiver manager not available")
                return
            
            sms_method = self.config.get_sms_method()
            
            if sms_method == "manual":
                messagebox.showinfo(
                    "Manual Mode",
                    "Manual entry mode doesn't require a receiver.\n\n"
                    "Select Google Voice or Email to enable automatic receiving."
                )
                return
            
            if sms_method not in ["google_voice", "email"]:
                messagebox.showinfo(
                    "Not Implemented",
                    f"{sms_method} receiver not yet implemented.\n\n"
                    "Available: Google Voice, Email"
                )
                return
            
            if main_window.receiver_manager.is_running():
                # Stop receiver
                main_window.receiver_manager.stop()
                messagebox.showinfo("Stopped", "SMS receiver stopped")
            else:
                # Start receiver
                main_window.receiver_manager.start(main_window.on_sms_received)
                messagebox.showinfo(
                    "Started",
                    f"SMS receiver started!\n\n"
                    f"Method: {sms_method}\n"
                    f"The app will now automatically check for incoming messages."
                )
            
            self.update_receiver_status()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle receiver: {str(e)}")
