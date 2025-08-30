from calendar import Calendar

def get_month_days(year, month):
    """
    Generate the calendar grid for a given year and month.
    Includes placeholders for days outside the current month.
    """
    cal = Calendar()
    return cal.monthdayscalendar(year, month)