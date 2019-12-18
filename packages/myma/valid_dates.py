import requests
import json
import datetime
import sqlite3
from sqlite3 import Error
from myma.date import Date
import time

# TODO: phase
def get_dates(target_date, N, stock_no, phase_shift='lag'):
  conn = None
  create_sql = "CREATE TABLE IF NOT EXISTS valid_dates (\
      date integer, stock_no integer, PRIMARY KEY (date, stock_no)\
  );"
  insert_sql = "INSERT INTO valid_dates(date, stock_no)\
      VALUES(strftime('%s', ?), ?)"
  lagphase_sql = "SELECT *\
      FROM valid_dates\
      WHERE stock_no = ? AND date < date(?, 'unixepoch')\
      ORDER BY date DESC\
      LIMIT ?;"
  zerophase_sql = "SELECT date(date, 'unixepoch')\
      FROM valid_dates\
      WHERE stock_no = ?\
      ORDER BY Abs(date - strftime('%s', ?)) ASC\
      LIMIT ?;"
  
  try:
    conn = sqlite3.connect('cache/myma.db')
    c = conn.cursor()
    c.execute(create_sql)
    db_max = next(c.execute("SELECT date(MAX(date), 'unixepoch') FROM valid_dates WHERE stock_no = ?", (stock_no,)))[0]
    db_min = next(c.execute("SELECT date(MIN(date), 'unixepoch') FROM valid_dates WHERE stock_no = ?", (stock_no,)))[0]
    select_sql = zerophase_sql
    res = [r[0] for r in c.execute(select_sql, (stock_no, str(target_date), N))]
  
    # TODO: what if target in the future
    shift_amt = 1#TODO: to prevent long suspension
    if db_max is None:
      fetch_date = target_date
    elif db_max in res:
      fetch_date = Date(db_max).shift(shift_amt, 'month')
    elif db_min in res:
      fetch_date = Date(db_min).shift(-shift_amt, 'month') # TODO what if min = 190102 => 0102 shouldn't in retval
    else:
      fetch_date = None
    print(fetch_date, db_max, db_min, res)

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
  date_s = str(date).replace('-', '')
  while True: # TODO: do not try forever
    try:
      r = requests.get(
          f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?\
              response=json&date={date_s}&stockNo={stock_no}')
      break
    except requests.exceptions.ConnectionError as e:
      if 'Connection aborted' in str(e):
        print('Connection error, waiting for retry...')
        time.sleep(10)
        continue
      else:
        assert False # TODO: handle
  page = r.text
  jsn = json.loads(page)
  dates = [Date(info[0]) for info in jsn['data']]
  return dates
