import pyperclip as copier
import sqlite3
from datetime import datetime
from time import strftime

class DateTime:
    def __init__(self, week = datetime.today().isocalendar()[1], day = strftime("%Y-%m-%d"), 
                 month = strftime("%Y-%m"), year = strftime("%Y"), current_weeks = None, combined = int(strftime("%Y%m%d%H%M")),
                   combined_date = None) -> None:
        self.week = week
        self.day = day
        self.month = month
        self.year = year
        self.current_weeks = current_weeks
        self.current_weeks = str(week) + str(year)
        self.combined = combined
        self.combined_date = combined_date

    def datedelta(self, start, end):
        date1 = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        date2 = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        delta = date2 - date1
        return delta
    @property
    def combinedDate(self):
        return [self.year, self.month, self.current_weeks, self.day, self.combined]
    
    def convert_to_seconds(self, datetime_str:str):
        # SPLIT WITH ,
        comma_split = datetime_str.split(",")
        if len(comma_split) == 2:
            days, hours = comma_split
            only_day_num = int(float(days.split(" ")[0]))
            hr, minute, sec = hours.split(":")
            hr = int(float(hr))
            minute = int(float(minute))
            sec = int(float(sec))
            seconds = (only_day_num * 86400) + (hr * 3600) + (minute*60) + sec
            return seconds
        elif len(comma_split) == 1:
            try:
                hr, minute, sec = comma_split[0].split(":")
                hr = int(float(hr))
                minute = int(float(minute))
                sec = int(float(sec))
                seconds = (hr * 3600) + (minute*60) + sec
                return seconds
            except ValueError:
                return "INVALID TOTAL TIME FORMAT"

def separate(numbers):
    floating = []
    new_str = ""
    float_pos = 0
    decision = ""
    sign_negative = ""
    str_num = str(numbers)
    listed = [i for i in str_num]
    original = listed

    try:
        if "." in str_num:
            float_pos += original.index(".")
            decision += "point"
            floating = listed[float_pos:]
        if "-" in str_num:
            listed.remove("-")
            sign_negative += "negative"

    except Exception:
        pass

    if decision == "point":
        listed = listed[:float_pos]

    if len(listed) > 3 and len(listed) < 7:
        try:
            position = len(listed) - 3
            listed.insert(position, " ")
        except Exception:
            pass

    elif len(listed) == 7:
        listed.insert(1, " ")
        listed.insert(5, " ")

    elif len(listed) == 8:
        listed.insert(2, " ")
        listed.insert(6, " ")

    elif len(listed) == 9:
        listed.insert(3, " ")
        listed.insert(7, " ")

    if sign_negative == "negative":
        new_str += "-"
    for j in listed:
        new_str += j
    if len(floating) > 0:
        for k in floating:
            new_str += k
    return new_str

def clipboard(data = None, action = None):
    if action == "copy" and data:
        copier.copy(data)
    elif action == "paste":
        return copier.paste()
    
class Database:
    def __init__(self, db_name) -> None:
        self.db = db_name
        self.conn = sqlite3.connect(self.db)
    
    @property
    def Conn(self):
        return self.conn

    def Table(self, cols:tuple, table_name:str):
        """cols: ('name TEXT', 'age INTEGER', 'school TEXT')"""
        conn = self.Conn
        cols = str(cols).replace("'", "")
        with conn:
            conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {cols}")

    def Insert(self, data, table_name):
        conn = self.Conn
        
        with conn:
            if type(data[0]) != list and type(data[0]) != tuple:
                place_holder = str(tuple(["?"] * len(data))).replace("'", "")
                conn.execute(f"INSERT INTO {table_name} VALUES {place_holder}", data)
            else:
                place_holder = str(tuple(["?"] * len(data[0]))).replace("'", "")
                conn.executemany(f"INSERT INTO {table_name} VALUES {place_holder}", data)
    
    def Select(self, table_name, cols, cond = None, check = None):
        """cols: `name, age`"""
        conn = self.Conn
        with conn:
            if not cond:
                obj = conn.execute(f"SELECT {cols} FROM {table_name}")
                return obj.fetchall()
            else:
                obj = conn.execute(f"SELECT {cols} FROM {table_name} WHERE {cond}", check)
                return obj.fetchall()
    
    def Update(self, table_name, cols_2_reset,check, cond = None):
        """cols_2_reset: `name=?, age=?`"""
        conn = self.Conn
        with conn:
            if not cond:
                conn.execute(f"UPDATE {table_name} SET {cols_2_reset}", check)
            else:
                conn.execute(f"UPDATE {table_name} SET {cols_2_reset} WHERE {cond}", check)
    
    def New_column(self, table_name, col_name_and_type):
        conn = self.Conn
        with conn:
            conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_name_and_type}")
        
    def Delete(self, table_name, cond = None):
        conn = self.Conn
        with conn:
            if not cond:
                conn.execute(f"DELETE FROM {table_name}")
            else:
                conn.execute(f"DELETE FROM {table_name} WHERE {cond}")

    def Columns(self, table_name):
        conn = self.Conn
        with conn:
            all_data = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
            return [(row[1], row[2]) for row in all_data]