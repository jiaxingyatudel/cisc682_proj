#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify

import pymysql

import time

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

    query=database.check_user_security_by_user_email(user_email)
    
    if(len(query)>0):
        resp=jsonify(
            err=1,#email already registered
            user_id=False
        )
        return resp
    else:
        user_info=database.insert_user_info(user_name)
        user_security=database.insert_user_security(user_info["user_id"],user_email,user_password)
        cookie=database.insert_user_cookie(user_info["user_id"])

        resp=jsonify(
            err=False,
            user_id=user_info["user_id"],
            user_name=user_info["user_name"],
            user_email=user_security["user_email"]
        )
        resp.set_cookie("user_cookie_value",cookie["user_cookie_value"])
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
        user_security=query[0]

        user_id=user_security["user_id"]
        user_email=user_security["user_email"]

        user_info=database.select_user_info_by_user_id(user_id)[0]
        cookie=database.insert_user_cookie(user_info["user_id"])

        resp=jsonify(
            err=0,
            user_id=user_info["user_id"],
            user_name=user_info["user_name"],
            user_email=user_security["user_email"]
        )
        resp.set_cookie("user_cookie_value",cookie["user_cookie_value"])
        return resp

@app.route("/check_user_cookie",methods=["POST"])
def check_user_cookie():
    user_cookie_value=request.cookies.get("user_cookie_value")

    query=database.check_user_cookie_by_user_cookie_value(user_cookie_value)

    if(len(query)>0):
        user_id=query[0]["user_id"]
        user_cookie_value=query[0]["user_cookie_value"]
        user_cookie_time_stamp=query[0]["user_cookie_time_stamp"]

        time_stamp_now=int(time.time())
        if((time_stamp_now-user_cookie_time_stamp)>7*24*60*60):
            #cookie time expire
            resp=jsonify(err=1)
            return resp
        else:
            database.update_user_cookie_by_user_cookie_value(user_cookie_value)

            user_info=database.select_user_info_by_user_id(user_id)[0]
            user_security=database.check_user_security_by_user_id(user_id)[0]

            resp=jsonify(
                err=0,
                user_id=user_info["user_id"],
                user_name=user_info["user_name"],
                user_email=user_security["user_email"]
            )
            return resp
    else:
        resp=jsonify(err=1)
        return resp

@app.route("/user_logout",methods=["POST"])
def user_logout():
    user_cookie_value=request.cookies.get("user_cookie_value")
    database.delete_user_cookie_by_user_cookie_value(user_cookie_value)
    resp=jsonify(err=0)
    resp.delete_cookie("user_cookie_value")
    return resp

if __name__ == '__main__':
    app.run()