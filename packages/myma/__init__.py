import datalab
from myma.date import Date

class Module(datalab.Module):
  def run(self, args):
    # TODO: automate this part by specifications of module
    assert len(args) == 3
    stock_id, date_str, N_str = args
    date = Date(date_str)
    N = int(N_str)

    for i in range(N):
      _date = date - i
      _path = f'twse.{stock_id}.{_date}.close'
      print(datalab.fetch(_path))
    return None
