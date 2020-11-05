#!/usr/bin/env python3

#This script inserts random data to database cisc637
#Use this script after initialize_database.py

import pymysql
from pymysql.constants import CLIENT

import random
import uuid
import hashlib
import datetime

from random_name_pool import RandomNamePool
from lorem_ipsum import LoremIpsum

USER_CNT=100
FOLLOW_USER_CNT_MIN=0
FOLLOW_USER_CNT_MAX=4
USER_POST_CNT_MIN=0
USER_POST_CNT_MAX=4

class UserPool:
    def __init__(self):
        self.users=[]

    def new_user_info(self,user_name,user_email):
        user=({
            "user_id":uuid.uuid4().hex,
            "user_name":user_name,
            "user_email":user_email
        })

        self.users.append(user)

        return user

class PostPool:
    def __init__(self):
        self.posts=[]

    def new_post_info(self,post_title,post_text,post_time,user_id):
        post=({
            "post_id":uuid.uuid4().hex,
            "post_title":post_title,
            "post_text":post_text,
            "post_time":post_time,
            "user_id":user_id
        })

        self.posts.append(post)

        return post

random_name_pool=RandomNamePool()

lorem_ipsum=LoremIpsum()

user_pool=UserPool()
post_pool=PostPool()

###

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

sql_insert_user_follow="""
insert into user_follow (user_id,follow_id) values ('{user_id}','{follow_id}');
"""

sql_insert_post_info="""
insert into post_info (post_id,post_title,post_text,post_time,user_id) values ('{post_id}','{post_title}','{post_text}','{post_time}','{user_id}');
"""

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

for i in range(len(user_pool.users)):
    user=user_pool.users[i]

    follow_user_cnt=random.randint(FOLLOW_USER_CNT_MIN,FOLLOW_USER_CNT_MAX)

    follow_user_index_pool=[]
    while(True):
        if len(follow_user_index_pool)>=follow_user_cnt:
            break
        follow_user_index=random.randint(0,len(user_pool.users)-1)
        if follow_user_index not in follow_user_index_pool:
            if follow_user_index!=i:
                follow_user_index_pool.append(follow_user_index)

    for j in range(len(follow_user_index_pool)):
        follow_user=user_pool.users[follow_user_index_pool[j]]
        cursor.execute(sql_insert_user_follow.format(user_id=user["user_id"],follow_id=follow_user["user_id"]))

for i in range(len(user_pool.users)):
    user=user_pool.users[i]
    post_cnt=random.randint(USER_POST_CNT_MIN,USER_POST_CNT_MAX)
    for j in range(post_cnt):
        post_title=lorem_ipsum.generate_sentence(4,8,6)
        post_text=lorem_ipsum.generate_paragraph(4,8,8,16,4)
        post_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post_pool.new_post_info(
            post_title,
            post_text,
            post_time,
            user["user_id"]
        )

for i in range(len(post_pool.posts)):
    post=post_pool.posts[i]
    cursor.execute(sql_insert_post_info.format(
        post_id=post["post_id"],
        post_title=post["post_title"],
        post_text=post["post_text"],
        post_time=post["post_time"],
        user_id=post["user_id"],
    ))

cursor.close()
conn.close()