import json
import pika
from flask import Blueprint, render_template, request
from models import ImageSQL, test_table

views = Blueprint("views", __name__)

# TODO Do we need to provide users with a way to key in their database credentials?
username = 'root'
password = 'root'
ip = 'localhost'
port = '3306'
table = 'Image'
imageSQL = ImageSQL(username, password, ip, port, table)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# RabbitMQ Queue Declaration
channel.queue_declare(queue='CaptionGen', durable=True)     # Request for caption generation
channel.queue_declare(queue='QuestGen', durable=True)       # Request for question generation
channel.queue_declare(queue='AnswerGen', durable=True)      # Request for answer generation


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
