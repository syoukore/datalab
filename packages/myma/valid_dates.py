import requests
import json
import datetime
import sqlite3
from sqlite3 import Error

#def run(N, up, down, mid):
stock_no = 2409
N = 50
target_date = 1020
conn = None
create_sql = "CREATE TABLE IF NOT EXISTS valid_dates (\
    date integer, stock_no integer, PRIMARY KEY (date, stock_no)\
);"
insert_sql = "INSERT INTO valid_dates(date, stock_no)\
    VALUES(?, ?)"
lagphase_sql = "SELECT *\
    FROM valid_dates\
    WHERE stock_no = ? AND date < ?\
    ORDER BY date DESC\
    LIMIT ?;"
zerophase_sql = "SELECT *\
    FROM valid_dates\
    WHERE stock_no = ?\
    ORDER BY Abs(date - ?) ASC\
    LIMIT ?;"

try:
  conn = sqlite3.connect('cache/myma.db')
  c = conn.cursor()
  c.execute(create_sql)
  #for i in range(1000, 1100):
  #  c.execute(insert_sql, (i, stock_no))
  #conn.commit()
  db_max = next(c.execute("SELECT MAX(date) FROM valid_dates WHERE stock_no = ?", (stock_no,)))[0]
  db_min = next(c.execute("SELECT MIN(date) FROM valid_dates WHERE stock_no = ?", (stock_no,)))[0]
  select_sql = zerophase_sql
  res = [r[0] for r in c.execute(select_sql, (stock_no, target_date, N))]

  if db_max is None:
    fetch_date = target_date
  elif db_max in res:
    fetch_date = target_date + 1
  elif db_min in res:
    fetch_date = target_date - 1
  else:
    print(res)
  print(fetch_date)
except Error as e:
  print(e)
finally:
  if conn:
    conn.close()
exit()

date = datetime.datetime(2019, 8, 2)
date_s = date.strftime("%Y%m%d")
r = requests.get(
    f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?\
        response=json&date={date_s}&stockNo={stock_no}')
page = r.text
jsn = json.loads(page)
dates = [info[0] for info in jsn['data']]
print(dates)
