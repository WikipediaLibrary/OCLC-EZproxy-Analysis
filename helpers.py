from datetime import timedelta


def date_range_list(start_date, end_date):
    # Return list of date objects between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date.strftime("%Y%m%d"))
        curr_date += timedelta(days=1)
    return date_list
