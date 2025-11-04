import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class StationDialog(ctk.CTkToplevel):
    def __init__(self, parent, db, station_data=None):
        super().__init__(parent)
        
        self.db = db
        self.station_data = station_data
        self.result = None
        
        self.title("Add Station" if not station_data else "Edit Station")
        self.geometry("400x450")
        self.resizable(True, True)
        self.minsize(350, 400)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
        if station_data:
            self.populate_fields()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        # Station Name
        ctk.CTkLabel(self, text="Station Name:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        self.name_entry = ctk.CTkEntry(self, placeholder_text="e.g., Station 1")
        self.name_entry.pack(pady=5, padx=20, fill="x")
        
        # Phone Number
        ctk.CTkLabel(self, text="Phone Number:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(15, 5), padx=20, anchor="w")
        self.phone_entry = ctk.CTkEntry(self, placeholder_text="e.g., +1234567890")
        self.phone_entry.pack(pady=5, padx=20, fill="x")
        
        # Min Value
        ctk.CTkLabel(self, text="Minimum Value:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(15, 5), padx=20, anchor="w")
        self.min_entry = ctk.CTkEntry(self, placeholder_text="e.g., 32.5")
        self.min_entry.pack(pady=5, padx=20, fill="x")
        
        # Max Value
        ctk.CTkLabel(self, text="Maximum Value:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(15, 5), padx=20, anchor="w")
        self.max_entry = ctk.CTkEntry(self, placeholder_text="e.g., 72.5")
        self.max_entry.pack(pady=5, padx=20, fill="x")
        
        # Enabled checkbox
        self.enabled_var = ctk.BooleanVar(value=True)
        self.enabled_check = ctk.CTkCheckBox(self, text="Monitoring Enabled", variable=self.enabled_var)
        self.enabled_check.pack(pady=15, padx=20, anchor="w")
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20, padx=20, fill="x")
        
        self.cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=self.cancel, fg_color="gray")
        self.cancel_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        self.save_btn = ctk.CTkButton(btn_frame, text="Save", command=self.save)
        self.save_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    def populate_fields(self):
        self.name_entry.insert(0, self.station_data['name'])
        self.phone_entry.insert(0, self.station_data['phone_number'])
        self.min_entry.insert(0, str(self.station_data['min_value']))
        self.max_entry.insert(0, str(self.station_data['max_value']))
        self.enabled_var.set(bool(self.station_data['enabled']))
    
    def save(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        min_val = self.min_entry.get().strip()
        max_val = self.max_entry.get().strip()
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Station name is required")
            return
        
        if not phone:
            messagebox.showerror("Error", "Phone number is required")
            return
        
        try:
            min_val = float(min_val)
            max_val = float(max_val)
        except ValueError:
            messagebox.showerror("Error", "Min and Max values must be numbers")
            return
        
        if min_val >= max_val:
            messagebox.showerror("Error", "Minimum value must be less than maximum value")
            return
        
        try:
            if self.station_data:
                # Update existing
                self.db.update_station(
                    self.station_data['id'],
                    name, phone, min_val, max_val,
                    self.enabled_var.get()
                )
            else:
                # Add new
                self.db.add_station(name, phone, min_val, max_val)
            
            self.result = True
            self.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "A station with this phone number already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save station: {str(e)}")
    
    def cancel(self):
        self.result = False
        self.destroy()


class StationsFrame(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.db = db
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Stations list
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header,
            text="Manage Stations",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")
        
        self.add_btn = ctk.CTkButton(
            header,
            text="➕ Add Station",
            command=self.add_station,
            width=120
        )
        self.add_btn.grid(row=0, column=1, padx=10)
    
    def refresh(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        stations = self.db.get_all_stations()
        
        if not stations:
            no_data = ctk.CTkLabel(
                self.scroll_frame,
                text="No stations configured.\nClick 'Add Station' to get started.",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_data.grid(row=0, column=0, pady=50)
            return
        
        for idx, station in enumerate(stations):
            self.create_station_row(station, idx)
    
    def create_station_row(self, station, row):
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=5, padx=5)
        frame.grid_columnconfigure(1, weight=1)
        
        # Status indicator
        status_color = "#4caf50" if station['enabled'] else "gray"
        status = ctk.CTkFrame(frame, width=5, fg_color=status_color)
        status.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0, 15))
        
        # Name
        name_label = ctk.CTkLabel(
            frame,
            text=station['name'],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 2))
        
        # Details
        details = f"📞 {station['phone_number']}  |  Range: {station['min_value']:.1f} - {station['max_value']:.1f}"
        details_label = ctk.CTkLabel(
            frame,
            text=details,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        details_label.grid(row=1, column=1, sticky="w", padx=10, pady=(2, 10))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            frame,
            text="✏️ Edit",
            command=lambda s=station: self.edit_station(s),
            width=80,
            height=30
        )
        edit_btn.grid(row=0, column=2, rowspan=2, padx=5)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            frame,
            text="🗑️",
            command=lambda s=station: self.delete_station(s),
            width=40,
            height=30,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        delete_btn.grid(row=0, column=3, rowspan=2, padx=5)
    
    def add_station(self):
        dialog = StationDialog(self, self.db)
        self.wait_window(dialog)
        if dialog.result:
            self.refresh()
    
    def edit_station(self, station):
        dialog = StationDialog(self, self.db, station)
        self.wait_window(dialog)
        if dialog.result:
            self.refresh()
    
    def delete_station(self, station):
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{station['name']}'?\nAll associated readings will be lost."
        )
        if result:
            self.db.delete_station(station['id'])
            self.refresh()
