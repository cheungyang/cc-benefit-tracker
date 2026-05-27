from datetime import date, timedelta
import calendar

def get_window_id(d: date, frequency: str) -> str:
    year = d.year
    month = d.month
    
    if frequency == 'monthly':
        return f"{year}-{month:02d}"
    elif frequency == 'quarterly':
        quarter = (month - 1) // 3 + 1
        return f"{year}-Q{quarter}"
    elif frequency == 'semiannually':
        half = 1 if month <= 6 else 2
        return f"{year}-H{half}"
    elif frequency == 'yearly':
        return f"{year}"
    return f"{year}-UNK"

def get_previous_window_id(d: date, frequency: str) -> str:
    if frequency == 'monthly':
        first_of_this_month = date(d.year, d.month, 1)
        last_day_of_prev_month = first_of_this_month - timedelta(days=1)
        return get_window_id(last_day_of_prev_month, frequency)
    elif frequency == 'quarterly':
        quarter = (d.month - 1) // 3 + 1
        first_of_this_quarter = date(d.year, (quarter-1)*3 + 1, 1)
        last_day_of_prev_quarter = first_of_this_quarter - timedelta(days=1)
        return get_window_id(last_day_of_prev_quarter, frequency)
    elif frequency == 'semiannually':
        half = 1 if d.month <= 6 else 2
        first_of_this_half = date(d.year, 1 if half == 1 else 7, 1)
        last_day_of_prev_half = first_of_this_half - timedelta(days=1)
        return get_window_id(last_day_of_prev_half, frequency)
    elif frequency == 'yearly':
        return str(d.year - 1)
    return "PREV-UNK"

def get_window_info(d: date, frequency: str) -> dict:
    year = d.year
    month = d.month
    
    reset_date = None
    
    if frequency == 'monthly':
        if month == 12:
            reset_date = date(year + 1, 1, 1)
        else:
            reset_date = date(year, month + 1, 1)
    elif frequency == 'quarterly':
        quarter = (month - 1) // 3 + 1
        if quarter == 4:
            reset_date = date(year + 1, 1, 1)
        else:
            reset_date = date(year, (quarter * 3) + 1, 1)
    elif frequency == 'semiannually':
        if month <= 6:
            reset_date = date(year, 7, 1)
        else:
            reset_date = date(year + 1, 1, 1)
    elif frequency == 'yearly':
        reset_date = date(year + 1, 1, 1)
    else:
        reset_date = date(year, month, 1) + timedelta(days=32)
        reset_date = date(reset_date.year, reset_date.month, 1)

    days_remaining = (reset_date - d).days
    
    return {
        "reset_date": reset_date,
        "days_remaining": days_remaining
    }
