import re
import datetime


DATE_EXP = "([0][1-9]|[12][0-9]|3[01])(\/|-)([0][1-9]|[1][0-2])(\/|-)(\d{4})"


def to_dt(str_date):
    if re.search('^\d{2}-\d{2}-\d{4}$', str_date):
        return datetime.datetime.strptime(str_date, "%d-%m-%Y")
    elif re.search('^\d{2}\/\d{2}\/\d{4}$', str_date):
        return datetime.datetime.strptime(str_date, "%d/%m/%Y")
    else:
        raise ValueError('The date is not properly built')


def cmp_dt(dateA, dateB):
    return (dateA - dateB).days
