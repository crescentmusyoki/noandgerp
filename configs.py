from datetime import timedelta, datetime
import random
import string

BID_STATUS = (('Open', 'Open'), ('Accepted', 'Accepted'), ('Denied', 'Denied'))

QUOTE_STATUS = (('Open', 'Open'), ('Accepted', 'Accepted'), ('Denied', 'Denied'))

DESIGN_TYPE = (('FEED', 'FEED'), ('HAZOP', 'HAZOP'), ('MODELING', 'MODELING'))

FABRICATION_STATUS = (('Ongoing', 'Ongoing'), ('Canceled', 'Canceled'), ('Complete', 'Complete'))

SURVEY_TYPE = (('Shipping', 'Shipping'), ('Fabrication', 'Fabrication'), ('Construction', 'Construction'))

QUESTION_TYPE = (('1', 'Yes/No'), ('2', 'Numerical'), ('3', 'Open Ended'))


def random_code(size=8, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size)).upper()


def random_number(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def date_to_datetime(date_val):
    return datetime.date(datetime.strptime(date_val, '%Y-%m-%d'))


# day min
def day_min(day_val):
    return datetime.combine(date_to_datetime(day_val), datetime.min.time())


# day max
def day_max(day_val):
    return datetime.combine(date_to_datetime(day_val), datetime.max.time())


# Split dates
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
