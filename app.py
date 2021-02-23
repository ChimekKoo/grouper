from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from random import shuffle

from utils import *
from constants import *
from cred import get_cred


cred = get_cred()

app = Flask(__name__)
app.secret_key = cred["secret-key"]

mongo_client = MongoClient(cred["mongodb-url"])
db = mongo_client["grouper"]
lists_col = db["lists"]
users_col = db["users"]


@app.route('/')
def index():
    if check_if_logged():
        return redirect(url_for("group"))
    else:
        return redirect(url_for("login"))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        try:
            request.form["login"]
            request.form["password"]
        except KeyError:
            return render_template("login.html", error="Wypełnij wszystkie pola.", logged=check_if_logged())
        else:
            if request.form["login"] == "" or request.form["password"] == "":
                return render_template("login.html", error="Wypełnij wszystkie pola.", logged=check_if_logged())
            else:

                result = cursor_to_list(users_col.find({
                    "login": request.form["login"],
                    "password": request.form["password"]
                }))

                if len(result) != 1:
                    return render_template("login.html", error="Nieprawidłowy login lub hasło.", logged=check_if_logged())
                else:

                    session["logged"] = True
                    return redirect(url_for("group"))

    elif request.method == "GET":
        if not check_if_logged():
            return render_template("login.html", logged=check_if_logged())
        else:
            return redirect(url_for("group"))


@app.route('/logout')
def logout():
    if check_if_logged():
        session.pop("logged", None)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route('/request-account')
def request_account():
    return render_template("request_account.html", logged=check_if_logged())


@app.route("/group", methods=["GET", "POST"])
def group():
    if request.method == "POST":

        try:
            request.form["list"]
            request.form["people_number"]
            request.form["equal_groups"]
        except KeyError:
            return render_template("group.html", error="Wypełnij wszystkie pola.", logged=check_if_logged())
        else:
            if request.form["list"] == "" or request.form["people_number"] == "":
                return render_template("group.html", error="Wypełnij wszystkie pola.", logged=check_if_logged())
            else:

                result = lists_col.find_one({
                    "name": request.form["list"]
                })

                if request.form["equal_groups"] == "on":
                    if len(result["students"])%request.form["people_number"] != 0:
                        return render_template("group.html", error="Nie da się utworzyć grupy.", logged=check_if_logged())

                shuffle(result)

                output = []


                lists = cursor_to_list(lists_col.find({}), "name")
                return render_template("group.html", lists=lists, logged=check_if_logged())

    elif request.method == "GET":
        lists = cursor_to_list(lists_col.find({}), "name")
        return render_template("group.html", lists=lists, logged=check_if_logged())


@app.route("/newlist", methods=["GET", "POST"])
def newlist():
    if request.method == "POST":
        pass
    elif request.method == "GET":
        pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=DEBUG)
