import requests
import json
import datetime
import sqlite3
from sqlite3 import Error
from myma.date import Date
import time

def get_dates(target_date, N, phase_shift='lag', stock_no='0050'):
  assert phase_shift == 'zero' or phase_shift == 'lag'
  assert type(target_date) is type(Date('2019-01-01'))
  conn = None
  create_sql = "CREATE TABLE IF NOT EXISTS valid_dates (\
      date integer PRIMARY KEY\
  );"
  insert_sql = "INSERT INTO valid_dates(date)\
      VALUES(strftime('%s', ?))"
  lagphase_sql = "SELECT date(date, 'unixepoch')\
      FROM valid_dates\
      WHERE date < strftime('%s', ?)\
      ORDER BY date DESC\
      LIMIT ?;"
  zerophase_sql = "SELECT date(date, 'unixepoch')\
      FROM valid_dates\
      ORDER BY Abs(date - strftime('%s', ?)) ASC\
      LIMIT ?;"
  
  res = None
  try:
    conn = sqlite3.connect('cache/myma.db')
    c = conn.cursor()
    c.execute(create_sql)
    while True:
      db_max_str = next(c.execute("SELECT date(MAX(date), 'unixepoch') FROM valid_dates"))[0]
      db_min_str = next(c.execute("SELECT date(MIN(date), 'unixepoch') FROM valid_dates"))[0]
      if db_max_str is None:
        fetch_date = target_date
      else:
        max_month = int(int(Date(db_max_str)) / 100)
        min_month = int(int(Date(db_min_str)) / 100)
        target_month = int(int(target_date) / 100)
        select_sql = zerophase_sql if phase_shift == 'zero' else lagphase_sql
        res = [r[0] for r in c.execute(select_sql, (str(target_date), N))]
        
        if min_month > target_month or target_month > max_month:
          fetch_date = target_date
        elif db_max_str in res:
          fetch_date = Date(db_max_str).shift(1, 'month')
        elif db_min_str in res:
          fetch_date = Date(db_min_str).shift(-1, 'month')
        elif len(res) < N: # sometimes needed for phase_shift = 'lag'
          fetch_date = target_date.shift(-1, 'month')
        else:
          fetch_date = None

      if fetch_date is None:
        break
      else:
        print(fetch_date, db_max_str, db_min_str, res)
        retval = crawl_date(fetch_date, stock_no)
        for d in retval:
          c.execute(insert_sql, (str(d),))
        conn.commit()
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
  return res
  
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
  assert jsn['stat'] == 'OK'
  dates = [Date(info[0]) for info in jsn['data']]
  return dates
