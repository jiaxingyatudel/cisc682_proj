#!/usr/bin/env python3

#This script initializes an empty database cisc637 and creates empty tables
#Any data previously in database cisc637 will be removed

import pymysql
from pymysql.constants import CLIENT

database_user=input("Please input database user name: ")
database_password=input("Please input database password: ")

conn=pymysql.connect(host="localhost",user=database_user,password=database_password,autocommit=True,client_flag=CLIENT.MULTI_STATEMENTS)
cursor=conn.cursor()

sql="""
drop database if exists cisc637;
create database cisc637;
use cisc637;

create table user_info(
    user_id varchar(255) primary key,
    user_name varchar(255)
);

create table user_security(
    user_id varchar(255) primary key,
    user_email varchar(255),
    user_password varchar(255)
);

create table user_follow(
    user_id varchar(255),
    follow_id varchar(255)
);

create table post_info(
    post_id varchar(255) primary key,
    post_title text,
    post_text text,
    post_time datetime,
    user_id varchar(255)
);

create table comment_info(
    comment_id varchar(255) primary key,
    comment_text text,
    comment_time datetime,
    target_id varchar(255),
    user_id varchar(255)
);

create table photo_info(
    photo_id varchar(255) primary key,
    photo_time varchar(255),
    user_id varchar(255)
);

create table post_photo(
    post_id varchar(255),
    photo_id varchar(255),
    photo_sequence int
);

create table tag_info(
    tag_id varchar(255) primary key,
    tag_name varchar(255)
);

create table post_tag(
    post_id varchar(255),
    tag_id varchar(255)
);
"""

cursor.execute(sql)

cursor.close()
conn.close()