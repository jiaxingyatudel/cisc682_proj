#!/usr/bin/env python3

#This script initializes an empty database cisc637 and creates empty tables
#Any data previously in database cisc637 will be removed

import pymysql
from pymysql.constants import CLIENT

import sql

database_user=input("[database user name]")
database_password=input("[database password]")
conn=pymysql.connect(host="localhost",user=database_user,password=database_password,autocommit=True,client_flag=CLIENT.MULTI_STATEMENTS)
cursor=conn.cursor()

cursor.execute(sql.sql_create_tables)

cursor.close()
conn.close()