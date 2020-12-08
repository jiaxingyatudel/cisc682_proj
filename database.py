#!/usr/bin/env python3

import pymysql

import uuid
import hashlib
import time

import sql

class Database:
    def __init__(self,database_user,database_password):
        conn=pymysql.connect(host="localhost",user=database_user,password=database_password,database="cisc637",autocommit=True)
        self.cursor=conn.cursor(pymysql.cursors.DictCursor)

    #user_info
    def insert_user_info(self,user_name):
        user_id=uuid.uuid4().hex
        self.cursor.execute(sql.sql_insert_user_info.format(user_id=user_id,user_name=user_name))
        return {
            "user_id":user_id,
            "user_name":user_name
        }

    def delete_user_info_by_user_id(self,user_id):
        self.cursor.execute(sql.sql_delete_user_info_by_user_id.format(user_id=user_id))

    def update_user_info_user_name_by_user_id(self,user_id,user_name):
        self.cursor.execute(sql.sql_update_user_info_user_name_by_user_id.format(user_id=user_id,user_name=user_name))

    def select_user_info_by_user_id(self,user_id):
        self.cursor.execute(sql.sql_select_user_info_by_user_id.format(user_id=user_id))
        return self.cursor.fetchall()

    #user_user_security
    def insert_user_security(self,user_id,user_email,user_password):
        user_password_hash=hashlib.sha256(user_password.encode("utf-8")).hexdigest()
        self.cursor.execute(sql.sql_insert_user_security.format(user_id=user_id,user_email=user_email,user_password=user_password_hash))
        return {
            "user_id":user_id,
            "user_email":user_email,
            "user_password":user_password
        }

    def update_user_security_user_email_by_user_id(self,user_id,user_email):
        self.cursor.execute(sql.sql_update_user_security_user_email_by_user_id.format(user_id=user_id,user_email=user_email))

    def update_user_security_user_password_by_user_id(self,user_id,user_password):
        user_password_hash=hashlib.sha256(user_password.encode("utf-8")).hexdigest()
        self.cursor.execute(sql.sql_update_user_security_user_password_by_user_id.format(user_id=user_id,user_password=user_password_hash))

    def check_user_security(self,user_email,user_password):
        user_password_hash=hashlib.sha256(user_password.encode("utf-8")).hexdigest()
        self.cursor.execute(sql.sql_select_user_security_by_user_email_user_password.format(user_email=user_email,user_password=user_password_hash))
        return self.cursor.fetchall()

    def check_user_security_by_user_email(self,user_email):
        self.cursor.execute(sql.sql_select_user_security_by_user_email.format(user_email=user_email))
        return self.cursor.fetchall()

    def check_user_security_by_user_id(self,user_id):
        self.cursor.execute(sql.sql_check_user_security_by_user_id.format(user_id=user_id))
        return self.cursor.fetchall()

    #user_cookie
    def insert_user_cookie(self,user_id):
        cookie=uuid.uuid4().hex
        time_stamp=int(time.time())
        self.cursor.execute(sql.sql_insert_user_cookie.format(user_id=user_id,user_cookie_value=cookie,user_cookie_time_stamp=time_stamp))
        return {
            "user_id":user_id,
            "user_cookie_value":cookie,
            "user_cookie_time_stamp":time_stamp
        }

    def check_user_cookie_by_user_cookie_value(self,user_cookie_value):
        self.cursor.execute(sql.sql_select_user_cookie_by_user_cookie_value.format(user_cookie_value=user_cookie_value))
        return self.cursor.fetchall()

    def update_user_cookie_by_user_cookie_value(self,user_cookie_value):
        time_stamp=int(time.time())
        self.cursor.execute(sql.sql_update_user_cookie_by_user_cookie_value.format(user_cookie_value=user_cookie_value,user_cookie_time_stamp=time_stamp))
        return {
            "user_cookie_value":user_cookie_value,
            "user_cookie_time_stamp":time_stamp
        }

    def delete_user_cookie_by_user_cookie_value(self,user_cookie_value):
        self.cursor.execute(sql.sql_delete_user_cookie_by_user_cookie_value.format(user_cookie_value=user_cookie_value))

    def delete_user_cookie_by_user_id(self,user_id):
        self.cursor.execute(sql.sql_delete_user_cookie_by_user_id.format(user_id=user_id))

    #user_follow
    #TODO

    #post_info
    #TODO

    #post_ingredient
    #TODO

    #user_like_post
    #TODO

    #comment_info
    #TODO

    #tag_info
    #TODO

    #post_tag
    #TODO

    #user_follow_tag
    #TODO

if __name__=="__main__":
    database_user=input("[database user name]")
    database_password=input("[database password]")

    database=Database(database_user,database_password)

    print(database.insert_user_info(input("[insert user info][user_name]")))
    print(database.delete_user_info_by_user_id(input("[delete user info][user_id]")))
    print(database.update_user_info_user_name_by_user_id(input("[update user info][user_id]"),input("[update user info][user_name]")))
    print(database.select_user_info_by_user_id(input("[slect user info][user_id]")))