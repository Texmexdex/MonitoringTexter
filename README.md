# Station Monitoring System

A desktop application for monitoring metric readings from multiple stations, with automatic alerts when values fall outside safe ranges.

## Features

- **Dashboard**: Real-time view of all stations with color-coded status indicators
- **Station Management**: Add, edit, and configure monitoring stations with custom safe ranges
- **Manual Entry**: Enter readings manually
- **History**: View complete reading history with filtering options
- **Settings**: Configure SMS integration (Twilio, Email, Webhook)
- **Alerts**: Automatic detection when readings fall outside safe ranges
- **Local Storage**: All data stored locally in SQLite database

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

1. **Add a Station**:
   - Go to "Manage Stations"
   - Click "Add Station"
   - Enter station name, phone number, and safe range (min/max values)
   - Click "Save"

2. **Enter a Reading**:
   - Go to "Manual Entry"
   - Select a station
   - Enter the value
   - Click "Submit Reading"

3. **View Dashboard**:
   - Go to "Dashboard" to see all stations
   - 🟢 Green = Normal, 🔴 Red = Alert

4. **Check History**:
   - Go to "History" to see all past readings
   - Filter by specific station

5. **Configure SMS Integration** (Optional):
   - Go to "Settings"
   - Choose your SMS reception method
   - Configure Twilio, Email, or Webhook
   - See `SMS_INTEGRATION_GUIDE.md` for details

## Project Structure

```
├── main.py                 # Application entry point
├── database.py            # SQLite database operations
├── message_parser.py      # Parse incoming text messages
├── requirements.txt       # Python dependencies
├── setup.bat              # Windows installation script
├── run.bat                # Windows launch script
└── gui/                   # User interface components
```

## Customization

### Message Parsing

Edit `message_parser.py` to handle different message formats. Current parser handles:
- "Station 1 - 56.893"
- "56.893"
- "Reading: 104.295"
- "Value is 72.5"

### UI Theme

Change appearance in the sidebar:
- Dark mode (default)
- Light mode
- System (follows OS setting)

## Troubleshooting

**App won't start**: Run `setup.bat` again

**Database errors**: Delete `monitoring.db` to reset (will lose all data)

**Import errors**: Make sure virtual environment is activated

## License

Free to use and modify for personal or commercial use.
