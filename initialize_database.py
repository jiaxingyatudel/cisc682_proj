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
    user_id varchar(255),
    user_name varchar(255),
    primary key (user_id)
);

create table user_security(
    user_id varchar(255),
    user_email varchar(255),
    user_password varchar(255),
    primary key (user_id),
    foreign key (user_id) references user_info(user_id) on delete cascade
);

create table user_follow(
    user_id varchar(255),
    follow_id varchar(255),
    foreign key (user_id) references user_info(user_id) on delete cascade,
    foreign key (follow_id) references user_info(user_id) on delete cascade
);

create table post_info(
    post_id varchar(255),
    post_title text,
    post_text text,
    post_time datetime,
    user_id varchar(255),
    primary key (post_id),
    foreign key (user_id) references user_info(user_id) on delete set null
);

create table comment_info(
    comment_id varchar(255),
    comment_text text,
    comment_time datetime,
    post_id varchar(255),
    user_id varchar(255),
    primary key (comment_id),
    foreign key (user_id) references user_info(user_id) on delete set null,
    foreign key (post_id) references post_info(post_id) on delete set null
);

create table photo_info(
    photo_id varchar(255),
    photo_time varchar(255),
    user_id varchar(255),
    primary key (photo_id),
    foreign key (user_id) references user_info(user_id) on delete set null
);

create table post_photo(
    post_id varchar(255),
    photo_id varchar(255),
    photo_sequence int,
    foreign key (post_id) references post_info(post_id) on delete set null,
    foreign key (photo_id) references photo_info(photo_id) on delete set null
);

create table tag_info(
    tag_id varchar(255),
    tag_name varchar(255),
    primary key (tag_id)
);

create table post_tag(
    post_id varchar(255),
    tag_id varchar(255),
    foreign key (post_id) references post_info(post_id) on delete set null,
    foreign key (tag_id) references tag_info(tag_id) on delete set null
);
"""

cursor.execute(sql)

cursor.close()
conn.close()