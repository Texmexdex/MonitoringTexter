import re
from typing import Optional, Tuple

class MessageParser:
    """Parse incoming text messages to extract metric values"""
    
    @staticmethod
    def parse_value(message: str) -> Optional[float]:
        """
        Extract numeric value from message.
        Handles formats like:
        - "Station 1 - 56.893"
        - "56.893"
        - "Reading: 104.295"
        - "Value is 72.5"
        """
        # Try to find decimal numbers
        patterns = [
            r'[-]?\d+\.\d+',  # Decimal number
            r'[-]?\d+',       # Integer
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                try:
                    return float(match.group())
                except ValueError:
                    continue
        
        return None
    
    @staticmethod
    def parse_station_and_value(message: str) -> Tuple[Optional[str], Optional[float]]:
        """
        Extract both station identifier and value from message.
        Returns (station_name, value)
        """
        # Try to extract station name/number
        station_match = re.search(r'station\s*(\d+|[a-zA-Z0-9]+)', message, re.IGNORECASE)
        station_name = station_match.group(1) if station_match else None
        
        # Extract value
        value = MessageParser.parse_value(message)
        
        return station_name, value
