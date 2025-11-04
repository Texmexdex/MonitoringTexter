import customtkinter as ctk
from tkinter import messagebox
from message_parser import MessageParser
from config import Config
from notifications import NotificationManager

class ManualEntryFrame(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.db = db
        self.parser = MessageParser()
        self.config = Config()
        self.notif_manager = NotificationManager(self.config)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Main content
        self.create_content()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header,
            text="Manual Entry",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        subtitle = ctk.CTkLabel(
            header,
            text="Manually enter readings for testing or when messages are received outside the system",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.pack(side="left", padx=20)
    
    def create_content(self):
        content = ctk.CTkFrame(self)
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        
        # Station selection
        station_label = ctk.CTkLabel(
            content,
            text="Select Station:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        station_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.station_var = ctk.StringVar()
        self.station_menu = ctk.CTkOptionMenu(
            content,
            variable=self.station_var,
            values=["No stations available"],
            command=self.on_station_select
        )
        self.station_menu.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        # Station info display
        self.info_frame = ctk.CTkFrame(content, fg_color="transparent")
        self.info_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            justify="left"
        )
        self.info_label.pack(anchor="w")
        
        # Value entry
        value_label = ctk.CTkLabel(
            content,
            text="Reading Value:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        value_label.grid(row=3, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.value_entry = ctk.CTkEntry(
            content,
            placeholder_text="Enter numeric value (e.g., 56.893)",
            font=ctk.CTkFont(size=14)
        )
        self.value_entry.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        # Raw message (optional)
        message_label = ctk.CTkLabel(
            content,
            text="Raw Message (Optional):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        message_label.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.message_text = ctk.CTkTextbox(
            content,
            height=100,
            font=ctk.CTkFont(size=12)
        )
        self.message_text.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        
        # Parse button
        parse_btn = ctk.CTkButton(
            content,
            text="📝 Parse Value from Message",
            command=self.parse_message,
            fg_color="gray",
            hover_color="#555"
        )
        parse_btn.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        
        # Submit button
        self.submit_btn = ctk.CTkButton(
            content,
            text="✅ Submit Reading",
            command=self.submit_reading,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.submit_btn.grid(row=8, column=0, padx=20, pady=30, sticky="ew")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            content,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=9, column=0, padx=20, pady=(0, 20))
    
    def refresh(self):
        stations = self.db.get_all_stations()
        
        if not stations:
            self.station_menu.configure(values=["No stations available"])
            self.station_var.set("No stations available")
            self.submit_btn.configure(state="disabled")
            return
        
        station_names = [f"{s['name']} ({s['phone_number']})" for s in stations]
        self.station_menu.configure(values=station_names)
        self.station_var.set(station_names[0])
        self.submit_btn.configure(state="normal")
        
        self.on_station_select(station_names[0])
    
    def on_station_select(self, selection):
        if selection == "No stations available":
            self.info_label.configure(text="")
            return
        
        # Extract station name from selection
        station_name = selection.split(" (")[0]
        stations = self.db.get_all_stations()
        station = next((s for s in stations if s['name'] == station_name), None)
        
        if station:
            info_text = f"📞 {station['phone_number']}\n"
            info_text += f"Safe Range: {station['min_value']:.1f} - {station['max_value']:.1f}"
            self.info_label.configure(text=info_text)
    
    def parse_message(self):
        message = self.message_text.get("1.0", "end-1c").strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to parse")
            return
        
        value = self.parser.parse_value(message)
        if value is not None:
            self.value_entry.delete(0, "end")
            self.value_entry.insert(0, str(value))
            self.status_label.configure(text=f"✅ Parsed value: {value}", text_color="green")
        else:
            messagebox.showwarning("Parse Failed", "Could not extract a numeric value from the message")
            self.status_label.configure(text="❌ Failed to parse value", text_color="red")
    
    def submit_reading(self):
        selection = self.station_var.get()
        if selection == "No stations available":
            messagebox.showerror("Error", "No stations configured")
            return
        
        # Get station
        station_name = selection.split(" (")[0]
        stations = self.db.get_all_stations()
        station = next((s for s in stations if s['name'] == station_name), None)
        
        if not station:
            messagebox.showerror("Error", "Station not found")
            return
        
        # Get value
        value_str = self.value_entry.get().strip()
        if not value_str:
            messagebox.showerror("Error", "Please enter a value")
            return
        
        try:
            value = float(value_str)
        except ValueError:
            messagebox.showerror("Error", "Value must be a number")
            return
        
        # Get raw message
        raw_message = self.message_text.get("1.0", "end-1c").strip()
        
        # Save reading
        reading_id = self.db.add_reading(station['id'], value, raw_message)
        
        # Check if alert
        is_alert = value < station['min_value'] or value > station['max_value']
        
        if is_alert:
            self.status_label.configure(
                text=f"⚠️ Reading saved - OUT OF RANGE!",
                text_color="#d32f2f"
            )
            
            # Send notifications
            station_data = {
                'name': station['name'],
                'phone_number': station['phone_number'],
                'min_value': station['min_value'],
                'max_value': station['max_value'],
                'value': value
            }
            
            results = self.notif_manager.send_alert(station_data, value)
            
            notif_msg = ""
            if results:
                sent = [method for method, success in results.items() if success]
                if sent:
                    notif_msg = f"\n\nNotifications sent via: {', '.join(sent)}"
            
            messagebox.showwarning(
                "Alert",
                f"Reading is out of range!\n\n"
                f"Value: {value:.2f}\n"
                f"Safe Range: {station['min_value']:.1f} - {station['max_value']:.1f}"
                f"{notif_msg}"
            )
        else:
            self.status_label.configure(
                text=f"✅ Reading saved - Normal",
                text_color="green"
            )
        
        # Clear form
        self.value_entry.delete(0, "end")
        self.message_text.delete("1.0", "end")
