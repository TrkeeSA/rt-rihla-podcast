import re
from datetime import datetime

def parse_date(date_raw_text):
    if not date_raw_text:
        return ""
    try:
        match = re.search(r"(\d{2}\.\d{2}\.\d{4})\s*\|\s*(\d{2}:\d{2})", date_raw_text)
        if match:
            date_part, time_part = match.groups()
            cleand = f"{date_part} {time_part}"
            dt = datetime.strptime(cleand, "%d.%m.%Y %H:%M")
            return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
        return date_raw_text
    except Exception:
        return date_raw_text