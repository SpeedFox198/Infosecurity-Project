import time
from datetime import datetime

def to_unix(timestamp:datetime) -> int:
    """
    Convert datetime object to unix time format

    Args:
        timestamp(datetime): timestamp to be converted

    Returns:
        int: Unix time format of timestamp
    """
    return int(time.mktime(timestamp))
