#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify

import pymysql

import hashlib

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

    user_password_hash=hashlib.sha256(user_password.encode("utf-8")).hexdigest()

    user_info=database.insert_user_info(user_name)

    user_id=user_info["user_id"]

    database.insert_user_security(user_id,user_email,user_password_hash)

    resp=jsonify(user_id=user_id,user_name=user_name,user_email=user_email)
    resp.set_cookie("user_id",user_id)
    return resp

if __name__ == '__main__':
    app.run()