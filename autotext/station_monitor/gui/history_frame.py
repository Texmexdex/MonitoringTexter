import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class ResolutionDialog(ctk.CTkToplevel):
    def __init__(self, parent, db, reading_data):
        super().__init__(parent)
        
        self.db = db
        self.reading_data = reading_data
        self.result = None
        
        self.title("Add Resolution Notes")
        self.geometry("500x400")
        self.resizable(True, True)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="📝 Document Resolution",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.pack(pady=(20, 10), padx=20)
        
        # Alert info
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(pady=10, padx=20, fill="x")
        
        station_name = self.reading_data.get('station_name', 'Unknown')
        value = self.reading_data.get('value', 0)
        min_val = self.reading_data.get('min_value', 0)
        max_val = self.reading_data.get('max_value', 0)
        
        info_text = f"Station: {station_name}\nValue: {value:.2f} (Range: {min_val:.1f} - {max_val:.1f})"
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        ).pack(anchor="w")
        
        # Resolved by
        ctk.CTkLabel(
            self,
            text="Resolved By:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(15, 5), padx=20, anchor="w")
        
        self.resolved_by_entry = ctk.CTkEntry(
            self,
            placeholder_text="Your name or initials"
        )
        self.resolved_by_entry.pack(pady=5, padx=20, fill="x")
        
        # Resolution notes
        ctk.CTkLabel(
            self,
            text="What was done to resolve this alert?",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(15, 5), padx=20, anchor="w")
        
        self.notes_text = ctk.CTkTextbox(
            self,
            height=150,
            font=ctk.CTkFont(size=11)
        )
        self.notes_text.pack(pady=5, padx=20, fill="both", expand=True)
        
        # Pre-fill if exists
        existing_notes = self.reading_data.get('resolution_notes', '')
        existing_by = self.reading_data.get('resolved_by', '')
        
        if existing_notes:
            self.notes_text.insert("1.0", existing_notes)
        if existing_by:
            self.resolved_by_entry.insert(0, existing_by)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20, padx=20, fill="x")
        
        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.cancel,
            fg_color="gray"
        )
        self.cancel_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Save Notes",
            command=self.save
        )
        self.save_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    def save(self):
        notes = self.notes_text.get("1.0", "end-1c").strip()
        resolved_by = self.resolved_by_entry.get().strip()
        
        if not notes:
            messagebox.showwarning("Warning", "Please enter resolution notes")
            return
        
        try:
            reading_id = self.reading_data['id']
            self.db.add_resolution_notes(reading_id, notes, resolved_by)
            self.result = True
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save notes: {str(e)}")
    
    def cancel(self):
        self.result = False
        self.destroy()


class HistoryFrame(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.db = db
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Content
        self.create_content()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header,
            text="Reading History",
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
    
    def create_content(self):
        content = ctk.CTkFrame(self)
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)
        
        # Station filter
        filter_frame = ctk.CTkFrame(content, fg_color="transparent")
        filter_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        filter_label = ctk.CTkLabel(
            filter_frame,
            text="Filter by Station:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        filter_label.pack(side="left", padx=(0, 10))
        
        self.station_var = ctk.StringVar(value="All Stations")
        self.station_filter = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.station_var,
            values=["All Stations"],
            command=lambda x: self.refresh()
        )
        self.station_filter.pack(side="left")
        
        # History list
        self.scroll_frame = ctk.CTkScrollableFrame(content)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh()
    
    def refresh(self):
        # Update station filter
        stations = self.db.get_all_stations()
        station_names = ["All Stations"] + [s['name'] for s in stations]
        self.station_filter.configure(values=station_names)
        
        # Clear history list
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Get selected station
        selected = self.station_var.get()
        
        if selected == "All Stations":
            # Get all readings
            all_readings = []
            for station in stations:
                readings = self.db.get_station_history(station['id'], limit=50)
                for reading in readings:
                    reading['station_name'] = station['name']
                    reading['station_phone'] = station['phone_number']
                    reading['min_value'] = station['min_value']
                    reading['max_value'] = station['max_value']
                all_readings.extend(readings)
            
            # Sort by date
            all_readings.sort(key=lambda x: x['received_at'], reverse=True)
            readings_to_show = all_readings[:100]  # Limit to 100 most recent
        else:
            # Get specific station
            station = next((s for s in stations if s['name'] == selected), None)
            if not station:
                return
            
            readings = self.db.get_station_history(station['id'], limit=100)
            readings_to_show = []
            for reading in readings:
                reading['station_name'] = station['name']
                reading['station_phone'] = station['phone_number']
                reading['min_value'] = station['min_value']
                reading['max_value'] = station['max_value']
                readings_to_show.append(reading)
        
        if not readings_to_show:
            no_data = ctk.CTkLabel(
                self.scroll_frame,
                text="No readings recorded yet.",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_data.grid(row=0, column=0, pady=50)
            return
        
        # Display readings
        for idx, reading in enumerate(readings_to_show):
            self.create_reading_row(reading, idx)
    
    def add_resolution_notes(self, reading):
        """Open dialog to add resolution notes"""
        dialog = ResolutionDialog(self, self.db, reading)
        self.wait_window(dialog)
        if dialog.result:
            self.refresh()
    
    def create_reading_row(self, reading, row):
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=3, padx=5)
        frame.grid_columnconfigure(1, weight=1)
        
        # Status indicator
        is_alert = reading.get('is_alert', 0)
        status_color = "#d32f2f" if is_alert else "#4caf50"
        status = ctk.CTkFrame(frame, width=5, fg_color=status_color)
        status.grid(row=0, column=0, rowspan=3, sticky="ns", padx=(0, 15))
        
        # Station name and time
        station_name = reading.get('station_name', 'Unknown')
        received_at = reading.get('received_at', '')
        
        try:
            dt = datetime.fromisoformat(received_at)
            # Show relative time if recent, otherwise full timestamp
            now = datetime.now()
            diff = now - dt
            
            if diff.total_seconds() < 60:
                time_str = "Just now"
            elif diff.total_seconds() < 3600:
                mins = int(diff.total_seconds() / 60)
                time_str = f"{mins} minute{'s' if mins != 1 else ''} ago"
            elif diff.total_seconds() < 86400:
                hours = int(diff.total_seconds() / 3600)
                time_str = f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif diff.days < 7:
                time_str = f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
            else:
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            
            # Add full timestamp in tooltip
            full_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            time_str = received_at
            full_time = received_at
        
        header_text = f"{station_name}  •  {time_str}"
        header_label = ctk.CTkLabel(
            frame,
            text=header_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        header_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 2))
        
        # Add full timestamp as smaller text
        try:
            full_time_label = ctk.CTkLabel(
                frame,
                text=f"({full_time})",
                font=ctk.CTkFont(size=9),
                text_color="gray",
                anchor="w"
            )
            full_time_label.grid(row=0, column=2, sticky="w", padx=5, pady=(10, 2))
        except:
            pass
        
        # Value
        value = reading.get('value', 0)
        min_val = reading.get('min_value', 0)
        max_val = reading.get('max_value', 0)
        
        value_text = f"Value: {value:.2f}  |  Range: {min_val:.1f} - {max_val:.1f}"
        value_label = ctk.CTkLabel(
            frame,
            text=value_text,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        value_label.grid(row=1, column=1, sticky="w", padx=10, pady=2)
        
        # Raw message if available
        raw_message = reading.get('raw_message', '')
        if raw_message:
            message_label = ctk.CTkLabel(
                frame,
                text=f"Message: {raw_message[:100]}{'...' if len(raw_message) > 100 else ''}",
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w"
            )
            message_label.grid(row=2, column=1, sticky="w", padx=10, pady=(2, 10))
        else:
            # Add padding
            spacer = ctk.CTkLabel(frame, text="")
            spacer.grid(row=2, column=1, pady=5)
        
        # Resolution notes if exists
        resolution_notes = reading.get('resolution_notes', '')
        if resolution_notes:
            resolved_by = reading.get('resolved_by', '')
            resolved_text = f"✓ Resolved"
            if resolved_by:
                resolved_text += f" by {resolved_by}"
            
            notes_label = ctk.CTkLabel(
                frame,
                text=resolved_text,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="green"
            )
            notes_label.grid(row=3, column=1, sticky="w", padx=10, pady=(2, 5))
            
            notes_content = ctk.CTkLabel(
                frame,
                text=f"Notes: {resolution_notes[:100]}{'...' if len(resolution_notes) > 100 else ''}",
                font=ctk.CTkFont(size=9),
                text_color="gray",
                anchor="w"
            )
            notes_content.grid(row=4, column=1, sticky="w", padx=10, pady=(0, 10))
        
        # Add notes button (for alerts)
        if is_alert:
            notes_btn = ctk.CTkButton(
                frame,
                text="📝 Notes" if not resolution_notes else "✏️ Edit",
                command=lambda r=reading: self.add_resolution_notes(r),
                width=80,
                height=25,
                fg_color="gray" if resolution_notes else "#2196F3",
                hover_color="#555" if resolution_notes else "#1976D2"
            )
            notes_btn.grid(row=0, column=3, rowspan=2, padx=5)
        
        # Status badge
        status_text = "⚠️ ALERT" if is_alert else "✅ Normal"
        status_badge = ctk.CTkLabel(
            frame,
            text=status_text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=status_color
        )
        status_badge.grid(row=0, column=4, rowspan=3, padx=15)
