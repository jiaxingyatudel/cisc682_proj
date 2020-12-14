#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file

import pymysql

import time
import datetime
import random
import os

from database import Database

database_host=input("[database host]")
database_user=input("[database user name]")
database_password=input("[database password]")
database=Database(database_host,database_user,database_password)

app=Flask(__name__,static_folder="./web/")

def check_user_auth_with_id(request,user_id):
    user_cookie_value=request.cookies.get("user_cookie_value")
    user_cookie_check=database.check_user_cookie_by_user_cookie_value(user_cookie_value)
    if((len(user_cookie_check)<1)or(user_cookie_check[0]["user_id"]!=user_id)):
        return False
    else:
        return True

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
    user_intro=req["user_intro"]

    query=database.check_user_security_by_user_email(user_email)
    
    if(len(query)>0):
        resp=jsonify(
            err=1,#email already registered
            user_id=False
        )
        return resp
    else:
        user_info=database.insert_user_info(user_name,user_intro)
        database.insert_user_security(user_info["user_id"],user_email,user_password)
        cookie=database.insert_user_cookie(user_info["user_id"])

        resp=jsonify(
            err=False,
            user_id=user_info["user_id"]
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
        cookie=database.insert_user_cookie(user_id)

        resp=jsonify(
            err=0,
            user_id=user_id
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

            resp=jsonify(
                err=0,
                user_id=user_id
            )
            return resp
    else:
        resp=jsonify(err=1)
        return resp

@app.route("/get_user_info_all",methods=["GET"])
def get_user_info_all():
    args=request.args

    user_id=args["user_id"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    user_info=database.select_user_info_by_user_id(user_id)[0]
    user_security=database.check_user_security_by_user_id(user_id)[0]

    resp=jsonify(
        err=0,
        user_id=user_info["user_id"],
        user_name=user_info["user_name"],
        user_intro=user_info["user_intro"],
        user_email=user_security["user_email"]
    )
    return resp

@app.route("/get_user_name_by_user_id",methods=["GET"])
def get_user_name_by_user_id():
    args=request.args

    user_id=args["user_id"]

    user_info=database.select_user_info_by_user_id(user_id)[0]

    resp=jsonify(
        err=0,
        user_id=user_info["user_id"],
        user_name=user_info["user_name"]
    )
    return resp

@app.route("/user_change_user_name",methods=["POST"])
def user_change_user_name():
    req=request.get_json(force=True)

    user_id=req["user_id"]
    user_name=req["user_name"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    database.update_user_info_user_name_by_user_id(user_id,user_name)

    resp=jsonify(
        err=0,
        user_name=user_name
    )
    return resp

@app.route("/user_change_user_email",methods=["POST"])
def user_change_user_email():
    req=request.get_json(force=True)

    user_id=req["user_id"]
    user_email=req["user_email"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    user_email_check=database.check_user_security_by_user_email(user_email)
    if(len(user_email_check)>0):
        #email already registered
        resp=jsonify(err=2)
        return resp

    database.update_user_security_user_email_by_user_id(user_id,user_email)

    resp=jsonify(
        err=0,
        user_email=user_email
    )
    return resp

@app.route("/user_change_user_intro",methods=["POST"])
def user_change_user_intro():
    req=request.get_json(force=True)

    user_id=req["user_id"]
    user_intro=req["user_intro"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    database.update_user_info_user_intro_by_user_id(user_id,user_intro)

    resp=jsonify(
        err=0,
        user_intro=user_intro
    )
    return resp

@app.route("/user_change_password",methods=["POST"])
def user_change_password():
    req=request.get_json(force=True)

    user_id=req["user_id"]
    user_email=req["user_email"]
    user_old_password=req["user_old_password"]
    user_new_password=req["user_new_password"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    user_security_check=database.check_user_security(user_email,user_old_password)
    if((len(user_security_check)<1) or (user_security_check[0]["user_id"]!=user_id)):
        #old password not match
        resp=jsonify(err=2)
        return resp

    database.update_user_security_user_password_by_user_id(user_id,user_new_password)
    resp=jsonify(err=0)
    return resp

@app.route("/user_logout",methods=["POST"])
def user_logout():
    user_cookie_value=request.cookies.get("user_cookie_value")
    database.delete_user_cookie_by_user_cookie_value(user_cookie_value)
    resp=jsonify(err=0)
    resp.delete_cookie("user_cookie_value")
    return resp

@app.route("/user_logout_all",methods=["POST"])
def user_logout_all():
    req=request.get_json(force=True)

    user_id=req["user_id"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    database.delete_user_cookie_by_user_id(user_id)
    resp=jsonify(err=0)
    resp.delete_cookie("user_cookie_value")
    return resp

@app.route("/get_following_users",methods=["GET"])
def get_following_users():
    args=request.args

    user_id=args["user_id"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    following_users_info=database.select_user_follow_join_user_info_by_user_id(user_id)

    resp=jsonify(
        err=0,
        following_users_info=following_users_info
    )
    return resp

@app.route("/check_user_following",methods=["GET"])
def check_user_following():
    args=request.args

    user_id=args["user_id"]
    my_user_id=args["my_user_id"]

    if not check_user_auth_with_id(request,my_user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    check_user_following=database.check_user_follow_by_user_id(my_user_id,user_id)

    resp=jsonify(
        err=0,
        user_following=(len(check_user_following)>0)
    )
    return resp

@app.route("/follow_user",methods=["POST"])
def follow_user():
    req=request.get_json(force=True)

    user_id=req["user_id"]
    my_user_id=req["my_user_id"]

    if not check_user_auth_with_id(request,my_user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    database.insert_user_follow(my_user_id,user_id)

    resp=jsonify(err=0)
    return resp

@app.route("/cancel_follow_user",methods=["POST"])
def cancel_follow_user():
    req=request.get_json(force=True)

    user_id=req["user_id"]
    my_user_id=req["my_user_id"]

    if not check_user_auth_with_id(request,my_user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    database.delete_user_follow_by_user_id_follow_id(my_user_id,user_id)

    resp=jsonify(err=0)
    return resp

def time_stamp_to_str(time_stamp):
    return datetime.datetime.utcfromtimestamp(time_stamp).strftime("%Y-%m-%dT%H:%M:%SZ")

def query_post_tags(post_id):
    return database.select_post_tag_info_of_post_id(post_id)

@app.route("/get_my_recipes_info",methods=["GET"])
def get_my_recipes_info():
    args=request.args

    user_id=args["user_id"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    my_recipes_info=database.select_post_info_join_user_info_by_user_id(user_id)

    for i in range(len(my_recipes_info)):
        post_info=my_recipes_info[i]
        post_info["post_time"]=time_stamp_to_str(post_info["post_time_stamp"])
        post_info["post_tags"]=query_post_tags(post_info["post_id"])

    resp=jsonify(
        err=0,
        my_recipes_info=my_recipes_info
    )
    return resp

@app.route("/get_user_recipes_info",methods=["GET"])
def get_user_recipes_info():
    args=request.args

    user_id=args["user_id"]
    my_user_id=args["my_user_id"]

    user_login=False

    if check_user_auth_with_id(request,my_user_id):
        #cookie check
        user_login=True

    user_recipes_info=database.select_post_info_join_user_info_by_user_id(user_id)

    for i in range(len(user_recipes_info)):
        post_info=user_recipes_info[i]
        post_info["post_time"]=time_stamp_to_str(post_info["post_time_stamp"])
        post_info["post_tags"]=query_post_tags(post_info["post_id"])

        if(user_login):
            post_like_check=database.check_user_like_post_by_user_id_post_id(my_user_id,post_info["post_id"])
            post_info["post_like"]=(len(post_like_check)>0)
        else:
            post_info["post_like"]=False

    resp=jsonify(
        err=0,
        user_recipes_info=user_recipes_info
    )
    return resp

@app.route("/get_liked_recipes_info",methods=["GET"])
def get_liked_recipes_info():
    args=request.args

    user_id=args["user_id"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    liked_recipes_info=database.select_post_info_join_user_info_join_user_like_post_by_user_id(user_id)

    for i in range(len(liked_recipes_info)):
        post_info=liked_recipes_info[i]
        post_info["post_time"]=time_stamp_to_str(post_info["post_time_stamp"])
        post_info["post_tags"]=query_post_tags(post_info["post_id"])
        post_info["post_like"]=True

    resp=jsonify(
        err=0,
        liked_recipes_info=liked_recipes_info
    )
    return resp

@app.route("/like_post",methods=["POST"])
def like_post():
    req=request.get_json(force=True)

    user_id=req["user_id"]
    post_id=req["post_id"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    database.insert_user_like_post(user_id,post_id)

    resp=jsonify(err=0)
    return resp

@app.route("/cancel_like_post",methods=["POST"])
def cancel_like_post():
    req=request.get_json(force=True)

    user_id=req["user_id"]
    post_id=req["post_id"]

    if not check_user_auth_with_id(request,user_id):
        #cookie check fail
        resp=jsonify(err=1)
        return resp

    database.delete_user_like_post_by_user_id_post_id(user_id,post_id)

    resp=jsonify(err=0)
    return resp

place_holder_img_dict={}
@app.route("/place_holder_img/<id>",methods=["GET"])
def place_holder_img(id):
    if id not in place_holder_img_dict:
        path_name="./web/img/"
        file_name=random.choice(os.listdir(path_name))
        place_holder_img_dict[id]=path_name+file_name

    return send_file(place_holder_img_dict[id])

if __name__ == '__main__':
    app.run()