import copy
import datetime
from dateutil.relativedelta import relativedelta
class Date:
  def __init__(self, date):
    if type(date) is type(1):
      date = str(date)
    if '-' in date or '/' in date:
      y, m, d = date.split('-') if '-' in date else date.split('/')
      assert len(y) == 3 or len(y) == 4 # taiwanese or western year
      y = int(y) if len(y) == 4 else int(y) + 1911
      date = str(y) + m + d
    assert len(date) == 8 # expected: yyyymmdd
    self.yyyy = int(date[:4])
    self.mm = int(date[4:6])
    self.dd = int(date[6:8])
    self.date = datetime.datetime(self.yyyy, self.mm, self.dd)

  def shift(self, amt, unit='day'):
    if 'year' == unit:
      delta = relativedelta(years=abs(amt))
    elif 'month' == unit:
      delta = relativedelta(months=abs(amt))
    else:
      delta = relativedelta(days=abs(amt))
    result = copy.copy(self)
    if amt < 0:
      result.date = self.date - delta
    else:
      result.date = self.date + delta
    result.yyyy = result.date.year
    result.mm = result.date.month
    result.dd = result.date.day
    return result

  def __str__(self):
    return self.date.strftime('%Y-%m-%d')

  def __repr__(self):
    return self.date.strftime('%Y-%m-%d')

