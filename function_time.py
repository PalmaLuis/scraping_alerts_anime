from datetime import datetime, timedelta
from hashlib import new
import pytz


# Retorna un datetime de acuerdo al horario de Perú
def change_time_peru(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%MZ")
    utc_zone = pytz.utc
    utc_time = utc_zone.localize(utc_time)
    peru_zone = pytz.timezone("America/Lima")
    local_time = utc_time.astimezone(peru_zone)
    # return local_time.strftime("%Y-%m-%d %I:%M %p")
    return local_time


def transform_format_twelve_str(time_peru):
    time_peru = time_peru.strftime("%Y-%m-%d %I:%M %p")
    return time_peru


now_peru = datetime.now(pytz.timezone("America/Lima"))
