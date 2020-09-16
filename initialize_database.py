#!/usr/bin/env python3

#This script initializes an empty database cisc637 and creates empty tables
#Any data previously in database cisc637 will be removed

import pymysql
from pymysql.constants import CLIENT

database_user=input("Please input database user name: ")
database_password=input("Please input database password: ")

conn=pymysql.connect(host="localhost",user=database_user,password=database_password,client_flag=CLIENT.MULTI_STATEMENTS)
cursor=conn.cursor()

sql="""
drop database if exists cisc637;
create database cisc637;
use cisc637;
"""

cursor.execute(sql)

cursor.close()
conn.close()