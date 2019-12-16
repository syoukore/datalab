import datalab
from myma.date import Date
from myma.valid_dates import get_dates

class Module(datalab.Module):
  def run(self, args):
    # TODO: automate this part by specifications of module
    assert len(args) == 3
    stock_no, date_str, N_str = args
    date = Date(date_str)
    N = int(N_str)
    get_dates(date, N, stock_no)

    #for i in range(N):
    #  _date = date - i
    #  _path = f'twse.{stock_no}.{_date}.close'
    #  print(datalab.fetch(_path))
    return None
