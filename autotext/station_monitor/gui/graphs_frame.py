import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime, timedelta

class GraphsFrame(ctk.CTkFrame):
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
            text="📈 Trend Graphs",
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
        
        # Controls
        controls = ctk.CTkFrame(content, fg_color="transparent")
        controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Station filter
        ctk.CTkLabel(
            controls,
            text="Station:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        self.station_var = ctk.StringVar(value="Select Station")
        self.station_filter = ctk.CTkOptionMenu(
            controls,
            variable=self.station_var,
            values=["Select Station"],
            command=lambda x: self.update_graph()
        )
        self.station_filter.pack(side="left", padx=(0, 20))
        
        # Time range filter
        ctk.CTkLabel(
            controls,
            text="Time Range:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        self.timerange_var = ctk.StringVar(value="Last 24 Hours")
        self.timerange_filter = ctk.CTkOptionMenu(
            controls,
            variable=self.timerange_var,
            values=["Last 6 Hours", "Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"],
            command=lambda x: self.update_graph()
        )
        self.timerange_filter.pack(side="left", padx=(0, 20))
        
        # Show range checkbox
        self.show_range_var = ctk.BooleanVar(value=True)
        self.show_range_check = ctk.CTkCheckBox(
            controls,
            text="Show Safe Range",
            variable=self.show_range_var,
            command=self.update_graph
        )
        self.show_range_check.pack(side="left", padx=(0, 20))
        
        # Graph container
        self.graph_container = ctk.CTkFrame(content)
        self.graph_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.graph_container.grid_columnconfigure(0, weight=1)
        self.graph_container.grid_rowconfigure(0, weight=1)
        
        # Initialize matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_container)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Stats panel
        self.stats_frame = ctk.CTkFrame(content)
        self.stats_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="Select a station to view statistics",
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        self.stats_label.pack(padx=15, pady=10, anchor="w")
        
        self.refresh()
    
    def refresh(self):
        """Refresh station list"""
        stations = self.db.get_all_stations()
        
        if not stations:
            self.station_filter.configure(values=["No stations available"])
            self.station_var.set("No stations available")
            self.show_no_data_message()
            return
        
        station_names = [s['name'] for s in stations]
        self.station_filter.configure(values=station_names)
        
        # Select first station if none selected
        if self.station_var.get() == "Select Station" or self.station_var.get() not in station_names:
            if station_names:
                self.station_var.set(station_names[0])
                self.update_graph()
    
    def update_graph(self):
        """Update the graph with current selection"""
        station_name = self.station_var.get()
        
        if station_name in ["Select Station", "No stations available"]:
            self.show_no_data_message()
            return
        
        # Get station
        stations = self.db.get_all_stations()
        station = next((s for s in stations if s['name'] == station_name), None)
        
        if not station:
            self.show_no_data_message()
            return
        
        # Get time range
        timerange = self.timerange_var.get()
        limit = self.get_limit_for_timerange(timerange)
        
        # Get readings
        readings = self.db.get_station_history(station['id'], limit=limit)
        
        if not readings:
            self.show_no_data_message("No readings available for this station")
            return
        
        # Filter by time range
        readings = self.filter_by_timerange(readings, timerange)
        
        if not readings:
            self.show_no_data_message("No readings in selected time range")
            return
        
        # Sort by time (oldest first for graph)
        readings.sort(key=lambda x: x['received_at'])
        
        # Extract data
        timestamps = []
        values = []
        
        for reading in readings:
            try:
                dt = datetime.fromisoformat(reading['received_at'])
                timestamps.append(dt)
                values.append(reading['value'])
            except:
                continue
        
        if not timestamps:
            self.show_no_data_message("Could not parse timestamps")
            return
        
        # Clear and plot
        self.ax.clear()
        
        # Plot readings
        self.ax.plot(timestamps, values, 'b-', linewidth=2, label='Readings', marker='o', markersize=4)
        
        # Plot safe range if enabled
        if self.show_range_var.get():
            min_val = station['min_value']
            max_val = station['max_value']
            
            self.ax.axhline(y=min_val, color='g', linestyle='--', linewidth=1.5, label=f'Min ({min_val:.1f})', alpha=0.7)
            self.ax.axhline(y=max_val, color='r', linestyle='--', linewidth=1.5, label=f'Max ({max_val:.1f})', alpha=0.7)
            
            # Fill safe range
            self.ax.fill_between(timestamps, min_val, max_val, alpha=0.1, color='green', label='Safe Range')
        
        # Formatting
        self.ax.set_xlabel('Time', fontsize=11, fontweight='bold')
        self.ax.set_ylabel('Value', fontsize=11, fontweight='bold')
        self.ax.set_title(f'{station_name} - Trend Over Time', fontsize=13, fontweight='bold')
        self.ax.legend(loc='best')
        self.ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
        self.figure.autofmt_xdate()
        
        # Tight layout
        self.figure.tight_layout()
        
        # Redraw
        self.canvas.draw()
        
        # Update statistics
        self.update_statistics(readings, station)
    
    def update_statistics(self, readings, station):
        """Update statistics panel"""
        if not readings:
            return
        
        values = [r['value'] for r in readings]
        
        # Calculate stats
        count = len(values)
        avg = sum(values) / count
        min_reading = min(values)
        max_reading = max(values)
        
        # Count alerts
        alerts = sum(1 for v in values if v < station['min_value'] or v > station['max_value'])
        alert_pct = (alerts / count * 100) if count > 0 else 0
        
        # Time range
        first_time = datetime.fromisoformat(readings[0]['received_at'])
        last_time = datetime.fromisoformat(readings[-1]['received_at'])
        time_span = last_time - first_time
        
        # Format stats
        stats_text = f"""
📊 Statistics for {station['name']}

Total Readings: {count}
Time Span: {self.format_timespan(time_span)}
First Reading: {first_time.strftime('%Y-%m-%d %H:%M:%S')}
Last Reading: {last_time.strftime('%Y-%m-%d %H:%M:%S')}

Average: {avg:.2f}
Minimum: {min_reading:.2f}
Maximum: {max_reading:.2f}

Safe Range: {station['min_value']:.1f} - {station['max_value']:.1f}
Alerts: {alerts} ({alert_pct:.1f}%)
Normal: {count - alerts} ({100 - alert_pct:.1f}%)
"""
        
        self.stats_label.configure(text=stats_text.strip())
    
    def format_timespan(self, td: timedelta) -> str:
        """Format timedelta as human-readable string"""
        days = td.days
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        
        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0 and days == 0:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        
        return ", ".join(parts) if parts else "< 1 minute"
    
    def get_limit_for_timerange(self, timerange: str) -> int:
        """Get database query limit for time range"""
        limits = {
            "Last 6 Hours": 500,
            "Last 24 Hours": 1000,
            "Last 7 Days": 2000,
            "Last 30 Days": 5000,
            "All Time": 10000
        }
        return limits.get(timerange, 1000)
    
    def filter_by_timerange(self, readings, timerange: str):
        """Filter readings by time range"""
        if timerange == "All Time":
            return readings
        
        now = datetime.now()
        cutoff_times = {
            "Last 6 Hours": now - timedelta(hours=6),
            "Last 24 Hours": now - timedelta(hours=24),
            "Last 7 Days": now - timedelta(days=7),
            "Last 30 Days": now - timedelta(days=30)
        }
        
        cutoff = cutoff_times.get(timerange)
        if not cutoff:
            return readings
        
        filtered = []
        for reading in readings:
            try:
                dt = datetime.fromisoformat(reading['received_at'])
                if dt >= cutoff:
                    filtered.append(reading)
            except:
                continue
        
        return filtered
    
    def show_no_data_message(self, message="No data to display"):
        """Show message when no data available"""
        self.ax.clear()
        self.ax.text(
            0.5, 0.5, message,
            horizontalalignment='center',
            verticalalignment='center',
            transform=self.ax.transAxes,
            fontsize=14,
            color='gray'
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
        
        self.stats_label.configure(text="Select a station with readings to view statistics")
