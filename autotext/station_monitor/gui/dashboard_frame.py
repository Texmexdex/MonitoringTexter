import customtkinter as ctk
from tkinter import messagebox
from typing import Dict

class StationCard(ctk.CTkFrame):
    def __init__(self, parent, station_data: Dict, on_call_click):
        super().__init__(parent, corner_radius=10)
        
        self.station_data = station_data
        self.on_call_click = on_call_click
        
        self.grid_columnconfigure(0, weight=1)
        
        # Status indicator
        status_color = self.get_status_color()
        self.status_indicator = ctk.CTkFrame(self, height=5, fg_color=status_color)
        self.status_indicator.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Station name
        name = station_data.get('name', 'Unknown')
        self.name_label = ctk.CTkLabel(
            self, 
            text=name,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.name_label.grid(row=1, column=0, padx=15, pady=(10, 5), sticky="w")
        
        # Current value
        value = station_data.get('value')
        if value is not None:
            value_text = f"{value:.2f}"
            status_text = self.get_status_text()
        else:
            value_text = "No data"
            status_text = "Waiting for data"
        
        self.value_label = ctk.CTkLabel(
            self,
            text=value_text,
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.value_label.grid(row=2, column=0, padx=15, pady=5)
        
        # Status text
        self.status_label = ctk.CTkLabel(
            self,
            text=status_text,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=3, column=0, padx=15, pady=5)
        
        # Range info
        min_val = station_data.get('min_value', 0)
        max_val = station_data.get('max_value', 0)
        range_text = f"Range: {min_val:.1f} - {max_val:.1f}"
        self.range_label = ctk.CTkLabel(
            self,
            text=range_text,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.range_label.grid(row=4, column=0, padx=15, pady=5)
        
        # Phone number
        phone = station_data.get('phone_number', '')
        self.phone_label = ctk.CTkLabel(
            self,
            text=f"📞 {phone}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.phone_label.grid(row=5, column=0, padx=15, pady=5)
        
        # Call button (only show if alert)
        if station_data.get('is_alert'):
            self.call_btn = ctk.CTkButton(
                self,
                text="📞 Call Technician",
                command=lambda: self.on_call_click(station_data),
                fg_color="#d32f2f",
                hover_color="#b71c1c"
            )
            self.call_btn.grid(row=6, column=0, padx=15, pady=(5, 15), sticky="ew")
        else:
            # Spacer
            spacer = ctk.CTkLabel(self, text="")
            spacer.grid(row=6, column=0, pady=10)
    
    def get_status_color(self):
        if not self.station_data.get('enabled'):
            return "gray"
        
        value = self.station_data.get('value')
        if value is None:
            return "gray"
        
        if self.station_data.get('is_alert'):
            return "#d32f2f"  # Red
        return "#4caf50"  # Green
    
    def get_status_text(self):
        if not self.station_data.get('enabled'):
            return "⏸️ Disabled"
        
        value = self.station_data.get('value')
        if value is None:
            return "⏳ No data"
        
        if self.station_data.get('is_alert'):
            min_val = self.station_data.get('min_value', 0)
            max_val = self.station_data.get('max_value', 0)
            if value < min_val:
                return "⚠️ Below minimum"
            else:
                return "⚠️ Above maximum"
        return "✅ Normal"


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.db = db
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Scrollable frame for station cards
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.scroll_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.refresh()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header,
            text="Station Dashboard",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")
        
        self.refresh_btn = ctk.CTkButton(
            header,
            text="🔄 Refresh",
            command=self.refresh,
            width=100
        )
        self.refresh_btn.grid(row=0, column=1, padx=10)
    
    def refresh(self):
        # Clear existing cards
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Get latest readings
        readings = self.db.get_latest_readings()
        
        if not readings:
            no_data = ctk.CTkLabel(
                self.scroll_frame,
                text="No stations configured.\nGo to 'Manage Stations' to add stations.",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_data.grid(row=0, column=0, columnspan=3, pady=50)
            return
        
        # Create cards in grid (3 columns)
        row = 0
        col = 0
        for reading in readings:
            card = StationCard(self.scroll_frame, reading, self.handle_call_click)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def handle_call_click(self, station_data):
        phone = station_data.get('phone_number', '')
        name = station_data.get('name', '')
        value = station_data.get('value', 0)
        min_val = station_data.get('min_value', 0)
        max_val = station_data.get('max_value', 0)
        
        message = f"Station: {name}\n"
        message += f"Phone: {phone}\n\n"
        message += f"Current Value: {value:.2f}\n"
        message += f"Safe Range: {min_val:.1f} - {max_val:.1f}\n\n"
        message += "Call technician to adjust?"
        
        result = messagebox.askyesno("Call Technician", message)
        if result:
            messagebox.showinfo("Call", f"Opening dialer for {phone}\n(Feature requires phone integration)\n\nTip: Go to History to document the resolution after calling.")
