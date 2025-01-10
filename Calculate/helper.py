from datetime import datetime


def interval_months(start: datetime, end: datetime):
    """
    当前利率下的总月数
    :return: Int,总月数
    """
    months = (end.year - start.year) * 12 + (end.month - start.month)
    return months
