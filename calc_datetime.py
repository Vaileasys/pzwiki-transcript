from datetime import datetime, timedelta

# determines the date and time from a timestamp based on an epoch
def timestamp_to_datetime(timestamp):
    timestamp = int(timestamp)
    epoch = datetime(1993, 7, 9)

    # Convert the timestamp (assumed to be in minutes) to a timedelta
    delta = timedelta(minutes=timestamp)

    # calculate the date and time
    new_datetime = epoch + delta

    # separate the date and time
    date_iso = new_datetime.date().isoformat() # date in ISO 8601 format
    time_24hr = new_datetime.strftime("%H:%M") # time in 24-hour format
    
    return time_24hr, date_iso

timestamp = 0  # timestamp to be converted into date & time
time, date = timestamp_to_datetime(timestamp)