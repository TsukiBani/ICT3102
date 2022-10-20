from flask import Blueprint, render_template,redirect,url_for, request

views = Blueprint('views', __name__)

@views.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        image = request.form['image_uploads']
        print(image)
    return render_template("index.html")
@views.route("/reviewimage",methods=["GET","POST"])
def reviewimage():
    return render_template("reviewimage.html")

@views.route("/searchimage")
def viewimage():
    return render_template("searchimage.html")