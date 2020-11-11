#!/usr/bin/env python3

from flask import Flask
from flask import request

app=Flask(__name__,static_folder="./web/")

@app.route('/',methods=["GET"])
def page():
    return app.send_static_file("app.html")

if __name__ == '__main__':
    app.run()