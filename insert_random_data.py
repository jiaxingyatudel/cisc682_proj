#!/usr/bin/env python3

#This script inserts random data to database cisc637
#Use this script after initialize_database.py

import pymysql
from pymysql.constants import CLIENT

database_user=input("Please input database user name: ")
database_password=input("Please input database password: ")

conn=pymysql.connect(host="localhost",user=database_user,password=database_password,client_flag=CLIENT.MULTI_STATEMENTS)
cursor=conn.cursor()

sql="""
use cisc637;
"""

cursor.execute(sql)

cursor.close()
conn.close()