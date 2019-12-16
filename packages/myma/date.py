import copy
import datetime
class Date:
  def __init__(self, d):
    if type(d) is type(1):
      d = str(d)
    assert len(d) == 8 # expected: yyyymmdd
    self.yyyy = int(d[:4])
    self.mm = int(d[4:6])
    self.dd = int(d[6:8])
    self.date = datetime.datetime(self.yyyy, self.mm, self.dd)

  def __sub__(self, other):
    if type(other) is type(1):
      other = datetime.timedelta(days=other)
    result = copy.copy(self)
    result.date = self.date - other
    result.yyyy = result.date.year
    result.mm = result.date.month
    result.dd = result.date.day
    return result

  def __str__(self):
    return self.date.strftime('%Y%m%d')
