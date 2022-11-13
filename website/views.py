from flask import Blueprint, render_template, redirect, url_for, request

from typing import List, Dict
from flask import Flask
import mysql.connector
import json

views = Blueprint("views", __name__)


def test_table() -> List[Dict]:
    config = {
        "user": "root",
        "password": "root",
        "host": "db",
        "port": "3306",
        "database": "02db",
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM test_table")
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    connection.close()

    return results


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
