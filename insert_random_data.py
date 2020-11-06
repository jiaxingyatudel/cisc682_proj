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
POST_COMMENT_CNT_MIN=0
POST_COMMENT_CNT_MAX=4
TAG_CNT=8
POST_TAG_CNT_MIN=1
POST_TAG_CNT_MAX=4

class UserPool:
    def __init__(self):
        self.users=[]

    def new_user_info(self,user_name,user_email):
        user={
            "user_id":uuid.uuid4().hex,
            "user_name":user_name,
            "user_email":user_email
        }
        self.users.append(user)
        return user

class PostPool:
    def __init__(self):
        self.posts=[]

    def new_post_info(self,post_title,post_text,post_time,user_id):
        post={
            "post_id":uuid.uuid4().hex,
            "post_title":post_title,
            "post_text":post_text,
            "post_time":post_time,
            "user_id":user_id
        }
        self.posts.append(post)
        return post

class CommentPool:
    def __init__(self):
        self.comments=[]

    def new_comment_info(self,comment_text,comment_time,post_id,user_id):
        comment={
            "comment_id":uuid.uuid4().hex,
            "comment_text":comment_text,
            "comment_time":comment_time,
            "post_id":post_id,
            "user_id":user_id,
        }
        self.comments.append(comment)
        return comment

class TagPool:
    def __init__(self):
        self.tags=[]

    def new_tag_info(self,tag_name):
        tag={
            "tag_id":uuid.uuid4().hex,
            "tag_name":tag_name
        }
        self.tags.append(tag)
        return tag

random_name_pool=RandomNamePool()

lorem_ipsum=LoremIpsum()

user_pool=UserPool()
post_pool=PostPool()
comment_pool=CommentPool()
tag_pool=TagPool()

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

sql_insert_comment_info="""
insert into comment_info (comment_id,comment_text,comment_time,user_id,post_id) values ('{comment_id}','{comment_text}','{comment_time}','{user_id}','{post_id}');
"""

sql_insert_tag_info="""
insert into tag_info (tag_id,tag_name) values ('{tag_id}','{tag_name}');
"""

sql_insert_post_tag="""
insert into post_tag (post_id,tag_id) values ('{post_id}','{tag_id}');
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

for i in range(len(post_pool.posts)):
    post=post_pool.posts[i]
    comment_cnt=random.randint(POST_COMMENT_CNT_MIN,POST_COMMENT_CNT_MAX)
    for j in range(comment_cnt):
        user=user_pool.users[random.randint(0,len(user_pool.users)-1)]
        comment_text=lorem_ipsum.generate_paragraph(2,4,8,16,4)
        comment_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_pool.new_comment_info(
            comment_text,
            comment_time,
            post["post_id"],
            user["user_id"]
        )

for i in range(len(comment_pool.comments)):
    comment=comment_pool.comments[i]
    cursor.execute(sql_insert_comment_info.format(
        comment_id=comment["comment_id"],
        comment_text=comment["comment_text"],
        comment_time=comment["comment_time"],
        user_id=comment["user_id"],
        post_id=comment["post_id"],
    ))

while(True):
    if len(tag_pool.tags)>=TAG_CNT:
        break

    tag_name=lorem_ipsum.lorem_ipsum_words[random.randint(9,len(lorem_ipsum.lorem_ipsum_words)-1)]

    tag_name_duplicate=False
    for i in range(len(tag_pool.tags)):
        if tag_name==tag_pool.tags[i]["tag_name"]:
            tag_name_duplicate=True
            break

    if not tag_name_duplicate:
        tag_pool.new_tag_info(tag_name.capitalize())

for i in range(len(tag_pool.tags)):
    tag=tag_pool.tags[i]
    cursor.execute(sql_insert_tag_info.format(
        tag_id=tag["tag_id"],
        tag_name=tag["tag_name"]
    ))

for i in range(len(post_pool.posts)):
    post=post_pool.posts[i]
    tag_cnt=random.randint(POST_TAG_CNT_MIN,POST_TAG_CNT_MAX)

    tag_index_pool=[]
    while(True):
        if(len(tag_index_pool)>=tag_cnt):
            break
        tag_index=random.randint(0,len(tag_pool.tags)-1)
        if(tag_index not in tag_index_pool):
            tag_index_pool.append(tag_index)

    for j in range(len(tag_index_pool)):
        tag=tag_pool.tags[tag_index_pool[j]]
        cursor.execute(sql_insert_post_tag.format(
            post_id=post["post_id"],
            tag_id=tag["tag_id"]
        ))

cursor.close()
conn.close()