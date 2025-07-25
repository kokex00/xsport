"""Timezone conversion utilities for different languages"""

import pytz
from datetime import datetime

# Language to timezone mapping
LANGUAGE_TIMEZONES = {
    "en": "GMT",  # English -> GMT
    "pt": "Europe/Lisbon",  # Portuguese -> Portugal time
    "es": "Europe/Madrid"   # Spanish -> Spain time
}

def convert_timezone(utc_datetime: datetime, language: str) -> str:
    """Convert UTC datetime to appropriate timezone based on language"""
    if not utc_datetime.tzinfo:
        utc_datetime = pytz.UTC.localize(utc_datetime)
    
    # Get target timezone based on language
    target_tz_name = LANGUAGE_TIMEZONES.get(language, "GMT")
    
    if target_tz_name == "GMT":
        target_tz = pytz.UTC
    else:
        target_tz = pytz.timezone(target_tz_name)
    
    # Convert to target timezone
    local_time = utc_datetime.astimezone(target_tz)
    
    # Format the time nicely
    if language == "en":
        return local_time.strftime("%Y-%m-%d %H:%M GMT")
    elif language == "pt":
        return local_time.strftime("%d/%m/%Y %H:%M (Portugal)")
    elif language == "es":
        return local_time.strftime("%d/%m/%Y %H:%M (España)")
    else:
        return local_time.strftime("%Y-%m-%d %H:%M UTC")

def get_current_time(language: str) -> str:
    """Get current time in appropriate timezone for language"""
    current_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
    return convert_timezone(current_utc, language)

def parse_time_string(time_str: str, language: str = "en") -> datetime:
    """Parse a time string and return UTC datetime"""
    try:
        # Parse the input time string (assuming local time for the language)
        local_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        
        # Get the timezone for the language
        tz_name = LANGUAGE_TIMEZONES.get(language, "GMT")
        
        if tz_name == "GMT":
            tz = pytz.UTC
        else:
            tz = pytz.timezone(tz_name)
        
        # Localize to the appropriate timezone
        localized_dt = tz.localize(local_dt)
        
        # Convert to UTC
        utc_dt = localized_dt.astimezone(pytz.UTC)
        
        return utc_dt
        
    except ValueError:
        raise ValueError(f"Invalid time format. Please use YYYY-MM-DD HH:MM")

def get_timezone_info(language: str) -> dict:
    """Get timezone information for a language"""
    tz_name = LANGUAGE_TIMEZONES.get(language, "GMT")
    
    if tz_name == "GMT":
        tz = pytz.UTC
        display_name = "GMT"
    else:
        tz = pytz.timezone(tz_name)
        display_name = tz_name
    
    current_time = datetime.now(tz)
    
    return {
        "timezone": tz_name,
        "display_name": display_name,
        "current_time": current_time.strftime("%Y-%m-%d %H:%M"),
        "offset": current_time.strftime("%z")
    }
