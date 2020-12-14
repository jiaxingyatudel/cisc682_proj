#!/usr/bin/env python3

#This script inserts random data to database cisc637
#Use this script after initialize_database.py

import pymysql

import random
import uuid
import hashlib
import time

from random_name_pool import RandomNamePool
from lorem_ipsum import LoremIpsum

import sql

USER_CNT=100
FOLLOW_USER_CNT_MIN=2
FOLLOW_USER_CNT_MAX=4
USER_POST_CNT_MIN=2
USER_POST_CNT_MAX=4
POST_INGREDIENT_CNT_MIN=4
POST_INGREDIENT_CNT_MAX=8
USER_LIKE_POST_CNT_MIN=4
USER_LIKE_POST_CNT_MAX=8
POST_COMMENT_CNT_MIN=2
POST_COMMENT_CNT_MAX=4
TAG_CNT=8
POST_TAG_CNT_MIN=1
POST_TAG_CNT_MAX=4
USER_FOLLOW_TAG_CNT_MIN=2
USER_FOLLOW_TAG_CNT_MAX=4

class UserPool:
    def __init__(self):
        self.users=[]

    def new_user_info(self,user_name,user_email,user_intro):
        user={
            "user_id":uuid.uuid4().hex,
            "user_name":user_name,
            "user_email":user_email,
            "user_intro":user_intro
        }
        self.users.append(user)
        return user

class PostPool:
    def __init__(self):
        self.posts=[]

    def new_post_info(self,post_title,post_text,post_time_stamp,user_id):
        post={
            "post_id":uuid.uuid4().hex,
            "post_title":post_title,
            "post_text":post_text,
            "post_time_stamp":post_time_stamp,
            "user_id":user_id,
            "post_title_img":"/place_holder_img/"+uuid.uuid4().hex
        }
        self.posts.append(post)
        return post

class CommentPool:
    def __init__(self):
        self.comments=[]

    def new_comment_info(self,comment_text,comment_time_stamp,post_id,user_id):
        comment={
            "comment_id":uuid.uuid4().hex,
            "comment_text":comment_text,
            "comment_time_stamp":comment_time_stamp,
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
database_host=input("[database host]")
database_user=input("[database user name]")
database_password=input("[database password]")
conn=pymysql.connect(host=database_host,user=database_user,password=database_password,database="cisc637",autocommit=True)
cursor=conn.cursor()

#user_info
#user_security
for i in range(USER_CNT):
    name=random_name_pool.generate_name()

    if not name:
        break

    user=user_pool.new_user_info(
        user_name="{first_name} {last_name}".format(first_name=name["first_name"],last_name=name["last_name"]),
        user_email="{first_name}.{last_name}@example.com".format(first_name=name["first_name"],last_name=name["last_name"]),
        user_intro=lorem_ipsum.generate_sentence(4,8,6)
    )

    user["user_password"]=hashlib.sha256("PASSWORD".encode("utf-8")).hexdigest()

for i in range(len(user_pool.users)):
    user=user_pool.users[i]
    cursor.execute(sql.sql_insert_user_info.format(user_id=user["user_id"],user_name=user["user_name"],user_intro=user["user_intro"]))
    cursor.execute(sql.sql_insert_user_security.format(user_id=user["user_id"],user_email=user["user_email"],user_password=user["user_password"]))

#user_follow
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
        cursor.execute(sql.sql_insert_user_follow.format(user_id=user["user_id"],follow_id=follow_user["user_id"]))

#post_info
for i in range(len(user_pool.users)):
    user=user_pool.users[i]
    post_cnt=random.randint(USER_POST_CNT_MIN,USER_POST_CNT_MAX)
    for j in range(post_cnt):
        post_title=lorem_ipsum.generate_sentence(4,8,6)
        post_text=lorem_ipsum.generate_paragraph(4,8,8,16,4)
        post_time_stamp=int(time.time())
        post_pool.new_post_info(
            post_title,
            post_text,
            post_time_stamp,
            user["user_id"]
        )

for i in range(len(post_pool.posts)):
    post=post_pool.posts[i]
    cursor.execute(sql.sql_insert_post_info.format(
        post_id=post["post_id"],
        post_title=post["post_title"],
        post_text=post["post_text"],
        post_title_img=post["post_title_img"],
        post_time_stamp=post["post_time_stamp"],
        user_id=post["user_id"],
    ))

#post_ingredient
for i in range(len(post_pool.posts)):
    post=post_pool.posts[i]
    ingredient_cnt=random.randint(POST_INGREDIENT_CNT_MIN,POST_INGREDIENT_CNT_MAX)
    ingredient_pool=random.sample(lorem_ipsum.lorem_ipsum_words,ingredient_cnt)
    for j in range(len(ingredient_pool)):
        ingredient=ingredient_pool[j]
        cursor.execute(sql.sql_insert_post_ingredient.format(
            post_id=post["post_id"],
            ingredient_id=uuid.uuid4().hex,
            ingredient_text=ingredient.capitalize(),
        ))

#user_like_post
for i in range(len(user_pool.users)):
    user=user_pool.users[i]
    like_post_cnt=random.randint(USER_LIKE_POST_CNT_MIN,USER_LIKE_POST_CNT_MAX)
    like_psot_sample=random.sample(post_pool.posts,like_post_cnt)
    for j in range(len(like_psot_sample)):
        post=like_psot_sample[j]
        cursor.execute(sql.sql_insert_user_like_post.format(
            user_id=user["user_id"],
            post_id=post["post_id"]
        ))

#comment_info
for i in range(len(post_pool.posts)):
    post=post_pool.posts[i]
    comment_cnt=random.randint(POST_COMMENT_CNT_MIN,POST_COMMENT_CNT_MAX)
    for j in range(comment_cnt):
        user=user_pool.users[random.randint(0,len(user_pool.users)-1)]
        comment_text=lorem_ipsum.generate_paragraph(2,4,8,16,4)
        comment_time_stamp=int(time.time())
        comment_pool.new_comment_info(
            comment_text,
            comment_time_stamp,
            post["post_id"],
            user["user_id"]
        )

for i in range(len(comment_pool.comments)):
    comment=comment_pool.comments[i]
    cursor.execute(sql.sql_insert_comment_info.format(
        comment_id=comment["comment_id"],
        comment_text=comment["comment_text"],
        comment_time_stamp=comment["comment_time_stamp"],
        user_id=comment["user_id"],
        post_id=comment["post_id"],
    ))

#tag_info
tag_name_pool=random.sample(lorem_ipsum.lorem_ipsum_words,TAG_CNT)
for i in range(len(tag_name_pool)):
    tag_name=tag_name_pool[i]
    tag_pool.new_tag_info(tag_name.capitalize())

for i in range(len(tag_pool.tags)):
    tag=tag_pool.tags[i]
    cursor.execute(sql.sql_insert_tag_info.format(
        tag_id=tag["tag_id"],
        tag_name=tag["tag_name"]
    ))

#post_tag
for i in range(len(post_pool.posts)):
    post=post_pool.posts[i]
    tag_cnt=random.randint(POST_TAG_CNT_MIN,POST_TAG_CNT_MAX)
    tag_sample=random.sample(tag_pool.tags,tag_cnt)
    for j in range(len(tag_sample)):
        tag=tag_sample[j]
        cursor.execute(sql.sql_insert_post_tag.format(
            post_id=post["post_id"],
            tag_id=tag["tag_id"]
        ))

#user_follow_tag
for i in range(len(user_pool.users)):
    user=user_pool.users[i]
    tag_cnt=random.randint(USER_FOLLOW_TAG_CNT_MIN,USER_FOLLOW_TAG_CNT_MAX)
    tag_sample=random.sample(tag_pool.tags,tag_cnt)
    for j in range(len(tag_sample)):
        tag=tag_sample[j]
        cursor.execute(sql.sql_insert_user_follow_tag.format(
            user_id=user["user_id"],
            tag_id=tag["tag_id"]
        ))

cursor.close()
conn.close()