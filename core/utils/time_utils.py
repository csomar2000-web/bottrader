from datetime import datetime, timezone

def now_utc():
    return datetime.now(timezone.utc)

def timestamp():
    return now_utc().isoformat()

def to_unix(dt):
    return int(dt.timestamp())
