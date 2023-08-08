from datetime import datetime
from dateutil import relativedelta

def depositCalculation(date, periods, amount, rate):
    startDate = datetime.strptime(date, "%d.%m.%Y").date()
    result = {}

    for i in range(periods):
        currentDate = startDate + relativedelta.relativedelta(months=+i)
        amount = round(amount * (1+rate/12/100), 2)
        result[datetime.strftime(currentDate, "%d.%m.%Y")] = amount

    return result