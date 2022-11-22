import json
import pika
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from website.models import ImageSQL,QuestionAnsSQL, test_table

views = Blueprint("views", __name__)

# TODO Do we need to provide users with a way to key in their database credentials?
username = 'root'
password = 'root'
ip = 'localhost'
port = '3306'
table = '02db'
imageSQL = ImageSQL(username, password, ip, port, table)
questionansSQL = QuestionAnsSQL(username, password, ip, port, table)

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# # RabbitMQ Queue Declaration
# channel.queue_declare(queue='CaptionGen', durable=True)  # Request for caption generation
# channel.queue_declare(queue='QuestGen', durable=True)  # Request for question generation
# channel.queue_declare(queue='AnswerGen', durable=True)  # Request for answer generation


@views.route("/", methods=["GET", "POST"])
def home() -> str:
    if request.method == "POST":
        nameOfImage = request.values.get('image_name')
        imageUrl = 'None'
        if imageSQL.doesImageNameExist(nameOfImage) == 1:
            # TODO How to reject duplicates?
            return render_template("index.html")
        else:
            imageID = imageSQL.insertImage(name=nameOfImage, image_url=imageUrl)
            session['id'] = imageID[0]
            return redirect(url_for('views.reviewimage'))
    return render_template("index.html")


@views.route("/reviewimage", methods=["GET", "POST"])
def reviewimage():
    ID = session['id']
    image = imageSQL.findById(ID)
    questionsql = questionansSQL.getDataByID(ID)
    if request.method == "POST":
        return render_template("reviewimage.html")
    # TODO Be able to update caption
    # TODO Be able to update question
    # TODO Be able to update answer
    return render_template("reviewimage.html", img_name=image[0],img_caption=image[2], qna = questionsql)

@views.route("/editcaption", methods = ["POST"])
def updatecaption():
    ID = session['id']
    image = imageSQL.findById(ID)
    if request.method == "POST":
        newcaptiondata = request.form["updatedvalue"]
        update = imageSQL.updatecaption(ID,newcaptiondata)
        return redirect(url_for("views.reviewimage"))
    return render_template("reviewimage.html", img_name=image[0],img_caption=image[2])
@views.route("/searchimage", methods=["GET", "POST"])
def viewimage():
    results = imageSQL.get_all()
    if request.method == "POST":
        session['id'] = request.values.get('image')
        return redirect(url_for('views.reviewimage'))
    return render_template("searchimage.html", results=results)

@views.route("/reviewimage/editqna", methods=["GET", "POST"])
def editqna():
    ID = session['id']
    image = imageSQL.findById(ID)
    if request.method == "POST":
        newcaptiondata = request.form["updatedvalue"]
        update = imageSQL.updatecaption(ID,newcaptiondata)
        return redirect(url_for("views.reviewimage"))
    return render_template("reviewimage.html", img_name=image[0],img_caption=image[2])
