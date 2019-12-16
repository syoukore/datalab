import requests
import json
import datetime
import sqlite3
from sqlite3 import Error
from myma.date import Date

def get_dates(target_date, N, stock_no, phase_shift='lag'):
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
    db_max = next(c.execute("SELECT MAX(date) FROM valid_dates WHERE stock_no = ?", (stock_no,)))[0]
    db_min = next(c.execute("SELECT MIN(date) FROM valid_dates WHERE stock_no = ?", (stock_no,)))[0]
    select_sql = zerophase_sql
    res = [r[0] for r in c.execute(select_sql, (stock_no, int(target_date), N))]
  
    if db_max is None:
      fetch_date = target_date
    elif db_max in res:
      fetch_date = Date(db_max) + 1
    elif db_min in res:
      fetch_date = Date(db_min) - 1 # TODO what if min = 190102 => 0102 shouldn't in retval, incremental month decrease (for long suspension)
    else:
      fetch_date = None
    print(fetch_date, db_max, db_min, res)
    # TODO FIXBUG: 190101 - 181231 should= 1

    if fetch_date is not None:
      retval = crawl_date(fetch_date, stock_no)
      for d in retval:
        c.execute(insert_sql, (str(d), stock_no))
      conn.commit()
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
  return
  
def crawl_date(date, stock_no):
  date_s = str(date)
  r = requests.get(
      f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?\
          response=json&date={date_s}&stockNo={stock_no}')
  page = r.text
  jsn = json.loads(page)
  dates = [Date(info[0]) for info in jsn['data']]
  return dates
