import json

from flask import Blueprint, render_template, request
from models import ImageSQL, test_table
import pika

views = Blueprint("views", __name__)
# TODO Do we need to provide users with a way to key in their database credentials?
username = 'root'
password = 'root'
ip = 'localhost'
port = '3306'
table = 'Image'
imageSQL = ImageSQL(username, password, ip, port, table)


@views.route("/", methods=["GET", "POST"])
def home() -> str:
    if request.method == "POST":
        image = request.form["image_uploads"]
        print(image)
    return render_template("index.html")


@views.route("/dbtest")
def dbtest() -> str:
    results = test_table()
    # return render_template("dbtest.html", results)
    return json.dumps({"test_table": test_table()})


@views.route("/reviewimage", methods=["GET", "POST"])
def reviewimage():
    return render_template("reviewimage.html")


@views.route("/searchimage")
def viewimage():
    return render_template("searchimage.html")
