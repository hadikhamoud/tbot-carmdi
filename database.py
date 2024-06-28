import sqlite3
import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(os.path.join(path, "CARMDI.db"), check_same_thread=False)
c = conn.cursor()

def search_cars(value):
    number, code = value.split()
    c.execute('SELECT * FROM CARMDI WHERE ActualNB = ? and CodeDesc = ?', (number, code.upper()))
    col_names = [cn[0] for cn in c.description]
    data = c.fetchall()
    return col_names, data

# def search_cars(query):
#     return [f"Car result for {query}"]

def search_phone_numbers(value):
    #select from CARMDI where TelProp like '%value%'
    c.execute('SELECT * FROM CARMDI WHERE TelProp LIKE ?', ('%'+value+'%',))
    col_names = [cn[0] for cn in c.description]
    data = c.fetchall()
    return col_names, data