#!/usr/bin/env python3

import pymysql

import uuid

sql_insert_user_info="""
insert into user_info (user_id,user_name) values ('{user_id}','{user_name}');
"""

sql_delete_user_info_by_user_id="""
delete from user_info where user_id='{user_id}';
"""

sql_update_user_info_user_name_by_user_id="""
update user_info set user_name='{user_name}' where user_id='{user_id}';
"""

sql_select_user_info_by_user_id="""
select * from user_info where user_id='{user_id}';
"""

sql_insert_user_security="""
insert into user_security (user_id,user_email,user_password) values ('{user_id}','{user_email}','{user_password}');
"""

class DatabaseQuery:
    def __init__(self,database_user,database_password):
        conn=pymysql.connect(host="localhost",user=database_user,password=database_password,database="cisc637",autocommit=True)
        self.cursor=conn.cursor(pymysql.cursors.DictCursor)

    def insert_user_info(self,user_name):
        user_id=uuid.uuid4().hex
        self.cursor.execute(sql_insert_user_info.format(user_id=user_id,user_name=user_name))
        return {
            "user_id":user_id,
            "user_name":user_name
        }

    def delete_user_info_by_user_id(self,user_id):
        self.cursor.execute(sql_delete_user_info_by_user_id.format(user_id=user_id))
        return {"user_id":user_id}

    def update_user_info_user_name_by_user_id(self,user_id,user_name):
        self.cursor.execute(sql_update_user_info_user_name_by_user_id.format(user_id=user_id,user_name=user_name))
        return {
            "user_id":user_id,
            "user_name":user_name
        }

    def select_user_info_by_user_id(self,user_id):
        self.cursor.execute(sql_select_user_info_by_user_id.format(user_id=user_id))
        return self.cursor.fetchall()

    def insert_user_security(self,user_id,user_email,user_password):
        self.cursor.execute(sql_insert_user_security.format(user_id=user_id,user_email=user_email,user_password=user_password))
        return {
            "user_id":user_id,
            "user_email":user_email,
            "user_password":user_password
        }


if __name__=="__main__":
    database_user=input("[database user name]")
    database_password=input("[database password]")

    database_query=DatabaseQuery(database_user,database_password)

    print(database_query.insert_user_info(input("[insert user info][user_name]")))
    print(database_query.delete_user_info_by_user_id(input("[delete user info][user_id]")))
    print(database_query.update_user_info_user_name_by_user_id(input("[update user info][user_id]"),input("[update user info][user_name]")))
    print(database_query.select_user_info_by_user_id(input("[slect user info][user_id]")))