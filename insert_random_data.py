#!/usr/bin/env python3

#This script inserts random data to database cisc637
#Use this script after initialize_database.py

import pymysql
from pymysql.constants import CLIENT

import random
import uuid
import hashlib

FAMILY_NAMES_FILE_PATH="./family_names.txt"
GIVEN_NAMES_FILE_PATH="./given_names.txt"

USER_CNT=100

class RandomNamePool:
    def __init__(self):
        self.used_names=[]

        family_names_file=open(FAMILY_NAMES_FILE_PATH,'r')
        self.family_name_list=[name.split('\n')[0] for name in family_names_file.readlines()]
        given_names_file=open(GIVEN_NAMES_FILE_PATH,'r')
        self.given_name_list=[name.split('\n')[0] for name in given_names_file.readlines()]
        family_names_file.close()
        given_names_file.close()

        self.capacity=len(self.family_name_list)*len(self.given_name_list)

    def generate_name(self):
        if len(self.used_names)>=self.capacity:
            return False

        while(True):
            name={
                "family_name":self.family_name_list[random.randint(0,len(self.family_name_list)-1)],
                "given_name":self.given_name_list[random.randint(0,len(self.given_name_list)-1)]
            }

            if name not in self.used_names:
                self.used_names.append(name)
                return name

class UserPool:
    def __init__(self):
        self.users=[]

    def new_user_info(self,user_name=False,user_email=False):
        user=({
            "user_id":uuid.uuid4().hex,
            "user_name":user_name,
            "user_email":user_email
        })

        self.users.append(user)

        return user

database_user=input("Please input database user name: ")
database_password=input("Please input database password: ")

conn=pymysql.connect(host="localhost",user=database_user,password=database_password,database="cisc637",autocommit=True,client_flag=CLIENT.MULTI_STATEMENTS)
cursor=conn.cursor()

sql_insert_user_info="""
insert into user_info (user_id,user_name) values ('{user_id}','{user_name}');
"""

sql_insert_user_security="""
insert into user_security (user_id,user_email,user_password) values ('{user_id}','{user_email}','{user_password}');
"""

random_name_pool=RandomNamePool()

user_pool=UserPool()

for i in range(USER_CNT):
    name=random_name_pool.generate_name()

    if not name:
        break

    user=user_pool.new_user_info(
        "{given_name} {family_name}".format(given_name=name["given_name"],family_name=name["family_name"]),
        "{given_name}.{family_name}@example.com".format(given_name=name["given_name"],family_name=name["family_name"])
    )

    user["user_password"]=hashlib.sha256("PASSWORD".encode("utf-8")).hexdigest()

for i in range(len(user_pool.users)):
    user=user_pool.users[i]
    cursor.execute(sql_insert_user_info.format(user_id=user["user_id"],user_name=user["user_name"]))
    cursor.execute(sql_insert_user_security.format(user_id=user["user_id"],user_email=user["user_email"],user_password=user["user_password"]))

cursor.close()
conn.close()