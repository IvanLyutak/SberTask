from datetime import datetime
from dateutil import relativedelta

def depositCalculation(date, periods, amount, rate):
    result = {}

    for i in range(periods):
        currentDate = date + relativedelta.relativedelta(months=+i)
        amount = round(amount * (1+rate/12/100), 2)
        result[datetime.strftime(currentDate, "%d.%m.%Y")] = amount

    return result