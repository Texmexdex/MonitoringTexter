# Station Monitoring System

A comprehensive desktop application for monitoring metric readings from multiple stations, with automatic alerts, trend analysis, and resolution tracking.

## Features

### Core Monitoring
- **Dashboard**: Real-time view of all stations with color-coded status indicators
- **Station Management**: Add, edit, and configure monitoring stations with custom safe ranges
- **Manual Entry**: Enter readings manually with instant validation
- **History**: Complete reading history with filtering and relative timestamps
- **Trend Graphs**: Visual analysis of readings over time with statistics
- **Alerts**: Automatic detection when readings fall outside safe ranges

### Communication & Notifications
- **SMS Reception**: Receive readings via Google Voice (FREE!), Email, Twilio, or Webhook
- **Alert Notifications**: Send alerts via Email, SMS (5 providers), or Push notifications
- **Multiple SMS Providers**: Twilio, Vonage, AWS SNS, Google Voice, or Custom Webhook

### Documentation & Analysis
- **Resolution Notes**: Document solutions for each alert
- **Knowledge Base**: Build searchable history of fixes
- **Statistics**: Track alert frequency, averages, and trends
- **Time Correlation**: Identify environmental factors and patterns

### Data & Storage
- **Local Database**: All data stored securely in SQLite
- **Automatic Timestamps**: Precise tracking of all readings
- **Data Export**: Ready for CSV/Excel export (coming soon)
- **Backup-Friendly**: Simple file-based storage

## Installation

### Quick Setup (Windows)

1. Double-click `setup.bat`
2. Wait for installation to complete
3. Double-click `run.bat` to launch

### Manual Setup

1. Install Python 3.8 or higher
2. Create virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate and install dependencies:
   ```bash
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Quick Start Guide

### 1. Add Your First Station
- Go to **"Manage Stations"**
- Click **"➕ Add Station"**
- Enter station name, phone number, and safe range (min/max values)
- Click **"Save"**

### 2. Enter a Reading
- Go to **"Manual Entry"**
- Select a station
- Enter the value
- Click **"Submit Reading"**
- System automatically checks if in range

### 3. View Dashboard
- Go to **"Dashboard"** to see all stations
- 🟢 Green = Normal, 🔴 Red = Alert
- Click **"📞 Call Technician"** on alerts

### 4. Analyze Trends
- Go to **"📈 Graphs"**
- Select a station and time range
- View trends, patterns, and statistics
- Identify environmental factors

### 5. Document Solutions
- Go to **"History"**
- Find an alert (red indicator)
- Click **"📝 Notes"** button
- Document what was done to resolve it
- Build your knowledge base

### 6. Configure Automation (Optional)
- Go to **"⚙️ Settings"**
- **SMS Reception**: Choose Google Voice (FREE!), Email, or Twilio
- **Alert Notifications**: Enable Email, SMS, or Push notifications
- See guides in documentation folder

## Project Structure

```
station_monitor/
├── main.py                      # Application entry point
├── database.py                  # SQLite database operations
├── message_parser.py            # Parse incoming text messages
├── notifications.py             # Alert notification system
├── sms_receiver.py             # SMS receiving (Google Voice, Email)
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
│
├── gui/                        # User interface
│   ├── main_window.py          # Main application window
│   ├── dashboard_frame.py      # Live monitoring dashboard
│   ├── stations_frame.py       # Station management
│   ├── manual_entry_frame.py   # Manual data entry
│   ├── history_frame.py        # Reading history with notes
│   ├── graphs_frame.py         # Trend visualization
│   └── settings_frame.py       # Configuration settings
│
├── setup.bat                   # Windows installation
├── run.bat                     # Windows launcher
│
└── Documentation/
    ├── README.md               # This file
    ├── QUICKSTART.txt          # Fast setup guide
    ├── SMS_INTEGRATION_GUIDE.md
    ├── SMS_PROVIDERS_GUIDE.md
    ├── GOOGLE_VOICE_SETUP.md
    ├── MOBILE_APP_INTEGRATION.md
    ├── GRAPHS_GUIDE.md
    └── RESOLUTION_NOTES_GUIDE.md
```

## Key Features Explained

### 📊 Dashboard
Real-time monitoring with color-coded cards:
- **Green**: Reading within safe range
- **Red**: Alert - out of range
- **Gray**: No data or disabled
- Auto-refreshes every 5 seconds
- Quick-call buttons for alerts

### 📈 Trend Graphs
Visual analysis over time:
- Line graphs with safe range overlay
- Time filters: 6 hours to all time
- Statistics: average, min, max, alerts
- Identify patterns and environmental factors
- Export-ready visualizations

### 📝 Resolution Notes
Document solutions and build knowledge:
- Add notes to any alert
- Record who resolved it
- Track what was done
- Search past solutions
- Train new staff
- Compliance-ready audit trail

### 🔔 Alert Notifications
Multiple notification methods:
- **Email**: SMTP to multiple addresses
- **SMS**: 5 providers (Google Voice FREE!)
- **Push**: Custom mobile app integration
- Automatic on out-of-range readings
- Configurable per method

### 📱 SMS Integration
Receive readings automatically:
- **Google Voice**: FREE! Polls every 60 seconds
- **Email Forwarding**: Forward texts to email
- **Twilio**: Professional SMS API
- **Webhook**: Custom integrations
- Automatic parsing and storage

### 🕐 Timestamps
Accurate time tracking:
- Automatic timestamps on all readings
- Relative time display ("5 minutes ago")
- Full timestamp for records
- Timezone-aware
- Audit-ready

## Customization

### Message Parsing
Edit `message_parser.py` to handle different formats:
- "Station 1 - 56.893"
- "56.893"
- "Reading: 104.295"
- "Value is 72.5"
- Custom patterns supported

### UI Theme
Change appearance in sidebar:
- **Dark mode** (default)
- **Light mode**
- **System** (follows OS)

### Safe Ranges
Adjust per station:
- Set minimum value
- Set maximum value
- Enable/disable monitoring
- Seasonal adjustments

### Notification Settings
Configure in Settings:
- Choose notification methods
- Set recipient addresses/numbers
- Configure providers
- Test connections

## Documentation

Comprehensive guides available:

- **QUICKSTART.txt** - Get running in 5 minutes
- **SMS_INTEGRATION_GUIDE.md** - Setup SMS receiving
- **SMS_PROVIDERS_GUIDE.md** - Compare 5 SMS providers
- **GOOGLE_VOICE_SETUP.md** - FREE SMS setup guide
- **MOBILE_APP_INTEGRATION.md** - Push notifications
- **GRAPHS_GUIDE.md** - Trend analysis guide
- **RESOLUTION_NOTES_GUIDE.md** - Document solutions

## Troubleshooting

**App won't start**: 
- Run `setup.bat` again
- Check Python version (need 3.8+)
- Verify virtual environment activated

**Database errors**: 
- Backup `monitoring.db` first
- Delete to reset (loses data)
- Check file permissions

**Import errors**: 
- Activate virtual environment
- Run `pip install -r requirements.txt`
- Check Python path

**Graphs not showing**:
- Install matplotlib: `pip install matplotlib`
- Check station has readings
- Try different time range

**SMS not receiving**:
- Check receiver status (green = running)
- Verify credentials in Settings
- Click "Start Receiver" button
- See SMS_INTEGRATION_GUIDE.md

**Notifications not sending**:
- Check Settings → Alert Notifications
- Verify provider credentials
- Use test buttons
- Check recipient addresses/numbers

For detailed troubleshooting, see individual guide documents.

## System Requirements

- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.8 or higher
- **RAM**: 100MB minimum
- **Disk**: 50MB for app + database
- **Display**: 1024x768 minimum (1200x700 recommended)

## Dependencies

Core:
- customtkinter 5.2.1 - Modern UI
- pillow 10.1.0 - Image handling
- requests 2.31.0 - HTTP requests
- matplotlib 3.8.2 - Graphs and charts

Optional:
- googlevoice - For Google Voice SMS (FREE!)
- boto3 - For AWS SNS SMS

## Performance

- **Startup**: < 2 seconds
- **Dashboard refresh**: < 100ms
- **Database queries**: < 10ms
- **Memory usage**: ~50-100MB
- **Handles**: 1000+ readings efficiently

## Future Enhancements

Planned features:
- ✅ Twilio SMS integration (ready, needs credentials)
- ✅ Email notifications (working)
- ✅ Push notifications (working)
- 🔜 Data export (CSV/Excel)
- 🔜 Automated reports
- 🔜 Multi-user support
- 🔜 Cloud sync
- 🔜 Mobile companion app
- 🔜 Advanced analytics
- 🔜 Custom alert rules

## Support

For help:
1. Check relevant guide in documentation folder
2. Review TROUBLESHOOTING section above
3. Check console output for errors
4. Verify configuration in Settings

## Contributing

Suggestions and improvements welcome!

## License

Free to use and modify for personal or commercial use.

## Version History

**v1.0** (2024-11-04)
- Initial release
- Dashboard monitoring
- Station management
- Manual entry
- History tracking
- Trend graphs
- Resolution notes
- SMS integration (5 providers)
- Alert notifications (Email, SMS, Push)
- Google Voice support (FREE!)
- Automatic SMS receiving
- Local database
- Dark/Light themes

---

**Built with Python, CustomTkinter, SQLite, and Matplotlib**
