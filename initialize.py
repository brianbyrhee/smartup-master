import mysql.connector
import collections
import csv
import pandas as pd
import pymysql
# connect to database

# import the module
from sqlalchemy import create_engine

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="ferhat437",
                               db="mydatabase"))

# declaring csv filename: you can do this as well if you have installed mysql on your laptop and replace the file name with your local csv
csvFile = 'ks-projects-201801.csv'

# organize headers for csv parsing- csv library reads a csv file as all strings, so you need to set the datatypes manually
col_names = pd.read_csv('kickstarterdata2018.csv', nrows=0).columns
types_dict = {'A': int, 'B': str, 'C': str, 'D': str, 'E': str, 'F': str, 'goal': float, 'launched': str,
			 'pledged': float, 'state': str, 'backers': int, 'country': str, 'usd1': float, 'usd2': float, 'usd3': str}
types_dict.update({col: str for col in col_names if col not in types_dict})
db = pd.read_csv('kickstarterdata2018.csv', dtype=types_dict)

# commented out, can print the dataframe to see what it is
print(db[:10])

# upload ENTIRE pandas dataframe to database
db.to_sql('projects', con = engine, if_exists = 'replace', chunksize = 1000)
