from datetime import datetime


def interval_months(start: datetime, end: datetime):
    """
    :param start: start date
    :param end: end date
    :return: the number of months between start and end
    """
    months = (end.year - start.year) * 12 + (end.month - start.month)
    return months
