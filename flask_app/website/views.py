import pika
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from website.models import ImageSQL, QuestionAnsSQL
from website.helper import captionGen
import os

views = Blueprint("views", __name__)

# TODO Do we need to provide users with a way to key in their database credentials?
username = "root"
password = "root"
ip = "db"
port = "3306"
table = "02db"
imageSQL = ImageSQL(username, password, ip, port, table)
questionansSQL = QuestionAnsSQL(username, password, ip, port, table)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="rabbitmq", heartbeat=600, blocked_connection_timeout=300
    )
)
channel = connection.channel()

# RabbitMQ Queue Declaration
channel.queue_declare(
    queue="CaptionGen", durable=True
)  # Request for caption generation
channel.queue_declare(queue="QuestGen", durable=True)  # Request for question generation
channel.queue_declare(queue="AnswerGen", durable=True)  # Request for answer generation


@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nameOfImage = request.values.get('image_name')
        imageUrl = os.environ.get("imagedb_RELATIVE_CONTAINER_PATH") + '/P1000654.JPG'
        if imageSQL.doesImageNameExist(nameOfImage) == 1:
            # TODO How to reject duplicates?
            return render_template("index.html")
        else:
            imageID = imageSQL.insertImage(name=nameOfImage, image_url=imageUrl)
            captionGen(str(imageID[0]))
            session['id'] = imageID[0]
            return redirect(url_for('views.reviewimage'))
    return render_template("index.html")


@views.route("/reviewimage", methods=["GET", "POST"])
def reviewimage():
    ID = session["id"]
    if ID:
        image = imageSQL.findById(ID)
        qnuestionsql = questionansSQL.getDataByID(ID)
        if not image and not qnuestionsql:
            flash("Insert not yet complete, please wait for a while before refreshing")
        return render_template("reviewimage.html", img_name=image[0], img_caption=image[2], qna=qnuestionsql)
    else:
        flash("No image or question not found")
        return redirect(url_for("views.home"))


@views.route("/editcaption", methods=["POST"])
def updatecaption():
    ID = session["id"]
    if ID:
        image = imageSQL.findById(ID)
        if request.method == "POST":
            if image:
                newcaptiondata = request.form["updatedvalue"]
                update = imageSQL.updatecaption(ID, newcaptiondata)
                if update:
                    flash("Caption updated successfully")
                else:
                    flash("Caption updated unsuccessfully")
            else:
                flash("Image not found")
    return render_template("reviewimage.html", img_name=image[0], img_caption=image[2])


@views.route("/searchimage", methods=["GET", "POST"])
def viewimage():
    results = imageSQL.get_all()
    if results:
        if request.method == "POST":
            session["id"] = request.values.get("image")
            return redirect(url_for("views.reviewimage"))
        return render_template("searchimage.html", results=results)
    else:
        flash("Images not found")
        return redirect(url_for("views.home"))


@views.route("/editqna", methods=["GET", "POST"])
def editqna():
    if request.method == "POST":
        questionid = request.form["questionID"]
        question = request.form["question"]
        answer = request.form["answer"]
        question_update = questionansSQL.updateQuestions(questionid, question)
        answer_update = questionansSQL.updateAnswers(questionid, answer)
        if not question_update and not answer_update:
            flash("Question or answer not updated successfully")
        else:
            flash("Question or answer updated successfully")
    return redirect(url_for("views.reviewimage"))
