from datetime import datetime

def datetime_to_str(datetime: datetime) -> str:
    return datetime.strftime(r"%Y-%m-%d %H:%M:%S")