import re
from datetime import datetime
from email.utils import format_datetime

def parse_date(date_raw_text):
    if not date_raw_text:
        return ""
    try:
        match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})\s*\|\s*(\d{2}):(\d{2})", date_raw_text)
        if match:
            day, month, year, hour, minute = match.groups()
            formatted_date = f"{year}-{month}-{day} {hour}:{minute}:00"
            return formatted_date

        return date_raw_text
    except Exception as e:
        print(f"Error parsing date: {e}")
        return date_raw_text


def format_date_for_rss(date_str_from_db):
    if not date_str_from_db:
        return ""
    try:
        dt = datetime.strptime(date_str_from_db, "%Y-%m-%d %H:%M:%S") 
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    except Exception:
        return date_str_from_db