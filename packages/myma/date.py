import copy
import datetime
class Date:
  def __init__(self, date):
    if type(date) is type(1):
      date = str(date)
    if '/' in date:
      y, m, d = date.split('/')
      assert len(y) == 3 or len(y) == 4 # taiwanese or western year
      y = int(y) if len(y) == 4 else int(y) + 1911
      date = str(y) + m + d
    assert len(date) == 8 # expected: yyyymmdd
    self.yyyy = int(date[:4])
    self.mm = int(date[4:6])
    self.dd = int(date[6:8])
    self.date = datetime.datetime(self.yyyy, self.mm, self.dd)

  def _datetime_op(self, other, op):
    if type(other) is type(1):
      other = datetime.timedelta(days=other)
    result = copy.copy(self)
    result.date = op(self.date, other)
    result.yyyy = result.date.year
    result.mm = result.date.month
    result.dd = result.date.day
    return result

  def __add__(self, other):
    return self._datetime_op(other, lambda x, y: x + y)

  def __sub__(self, other):
    return self._datetime_op(other, lambda x, y: x - y)

  def __str__(self):
    return self.date.strftime('%Y%m%d')

  def __repr__(self):
    return self.date.strftime('%Y%m%d')

  def __int__(self):
    return int(str(self))
