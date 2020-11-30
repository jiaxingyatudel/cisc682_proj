#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify

import pymysql

from database_query import DatabaseQuery

database_user=input("[database user name]")
database_password=input("[database password]")
database=DatabaseQuery(database_user,database_password)

app=Flask(__name__,static_folder="./web/")

@app.route("/",methods=["GET"])
def page():
    return app.send_static_file("app.html")

#api
@app.route("/user_register",methods=["POST"])
def user_register():
    req=request.get_json(force=True)
    user_name=req["user_name"]
    user_email=req["user_email"]
    user_password=req["user_password"]

    query=database.check_user_security_email(user_email)
    
    if(len(query)>0):
        resp=jsonify(
            err=1,#email already registered
            user_id=False
        )
        return resp
    else:
        user_info=database.insert_user_info(user_name)
        user_id=user_info["user_id"]

        database.insert_user_security(user_id,user_email,user_password)

        resp=jsonify(
            err=False,
            user_id=user_id,
            user_name=user_name,
            user_email=user_email
        )
        return resp

@app.route("/user_login",methods=["POST"])
def user_login():
    req=request.get_json(force=True)
    user_email=req["user_email"]
    user_password=req["user_password"]

    query=database.check_user_security(user_email,user_password)

    if(len(query)<=0):
        resp=jsonify(
            err=1,#no match found
            user_id=False
        )
        return resp
    else:
        user_id=query[0]["user_id"]
        user_email=query[0]["user_email"]

        user_info=database.select_user_info_by_user_id(user_id)[0]
        user_name=user_info["user_name"]

        resp=jsonify(
            err=0,
            user_id=user_id,
            user_name=user_name,
            user_email=user_email
        )
        return resp

if __name__ == '__main__':
    app.run()