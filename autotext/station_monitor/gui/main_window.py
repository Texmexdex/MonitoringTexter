import customtkinter as ctk
from tkinter import messagebox
from database import Database
from config import Config
from gui.dashboard_frame import DashboardFrame
from gui.stations_frame import StationsFrame
from gui.manual_entry_frame import ManualEntryFrame
from gui.history_frame import HistoryFrame
from gui.graphs_frame import GraphsFrame
from gui.settings_frame import SettingsFrame

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Station Monitoring System")
        self.geometry("1200x700")
        self.minsize(800, 600)
        
        # Initialize database and config
        self.db = Database()
        self.config = Config()
        
        # Initialize SMS receiver
        from sms_receiver import ReceiverManager
        self.receiver_manager = ReceiverManager(self.config, self.db)
        
        # Start receiver if configured
        sms_method = self.config.get_sms_method()
        if sms_method in ["google_voice", "email"]:
            self.receiver_manager.start(self.on_sms_received)
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Initialize frames
        self.frames = {}
        self.create_frames()
        
        # Show dashboard by default
        self.show_frame("dashboard")
        
        # Start auto-refresh
        self.auto_refresh()
    
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="📊 Monitor", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Navigation buttons
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar, 
            text="Dashboard",
            command=lambda: self.show_frame("dashboard"),
            height=40
        )
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_stations = ctk.CTkButton(
            self.sidebar,
            text="Manage Stations",
            command=lambda: self.show_frame("stations"),
            height=40
        )
        self.btn_stations.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_manual = ctk.CTkButton(
            self.sidebar,
            text="Manual Entry",
            command=lambda: self.show_frame("manual"),
            height=40
        )
        self.btn_manual.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_history = ctk.CTkButton(
            self.sidebar,
            text="History",
            command=lambda: self.show_frame("history"),
            height=40
        )
        self.btn_history.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_graphs = ctk.CTkButton(
            self.sidebar,
            text="📈 Graphs",
            command=lambda: self.show_frame("graphs"),
            height=40
        )
        self.btn_graphs.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_settings = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Settings",
            command=lambda: self.show_frame("settings"),
            height=40,
            fg_color="gray",
            hover_color="#555"
        )
        self.btn_settings.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        
        # Appearance mode
        self.appearance_label = ctk.CTkLabel(self.sidebar, text="Appearance:", anchor="w")
        self.appearance_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.appearance_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Dark", "Light", "System"],
            command=self.change_appearance
        )
        self.appearance_menu.grid(row=8, column=0, padx=20, pady=(0, 20))
        self.appearance_menu.set("Dark")
    
    def create_frames(self):
        self.frames["dashboard"] = DashboardFrame(self.main_frame, self.db)
        self.frames["stations"] = StationsFrame(self.main_frame, self.db)
        self.frames["manual"] = ManualEntryFrame(self.main_frame, self.db)
        self.frames["history"] = HistoryFrame(self.main_frame, self.db)
        self.frames["graphs"] = GraphsFrame(self.main_frame, self.db)
        self.frames["settings"] = SettingsFrame(self.main_frame, self.db, self.config)
        
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()
    
    def change_appearance(self, mode):
        ctk.set_appearance_mode(mode.lower())
    
    def auto_refresh(self):
        """Auto-refresh dashboard every 5 seconds"""
        if hasattr(self.frames["dashboard"], 'refresh'):
            self.frames["dashboard"].refresh()
        self.after(5000, self.auto_refresh)
    
    def on_sms_received(self, station, value, message):
        """Callback when SMS is received"""
        print(f"SMS received from {station['name']}: {value}")
        # Refresh dashboard to show new reading
        if hasattr(self.frames["dashboard"], 'refresh'):
            self.frames["dashboard"].refresh()
    
    def destroy(self):
        """Clean up when closing"""
        if hasattr(self, 'receiver_manager'):
            self.receiver_manager.stop()
        super().destroy()
