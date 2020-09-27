#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, render_template, abort, url_for
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    database = os.getenv("DATABASE")
)

c = db.cursor()

@app.route("/")
def page():
    return render_template("new.html", Title = "Short URL")

@app.route("/s/<slug>")
def page_redirect(slug):
    c.execute("SELECT url FROM urls WHERE slug = %(s)s;", { "s": slug })
    url = c.fetchone()
    if url is None:
        return redirect(url_for("page_error"))
    redirect_url = url[0]
    if redirect_url.find("http") == -1:
        redirect_url = "http://" + redirect_url
    return redirect(redirect_url)

@app.route("/error")
def page_error():
    return render_template("error.html", Title = "Error")

"""
Init database for first usage.
"""
def init_db():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS urls (id INT NOT NULL AUTO_INCREMENT, slug TEXT NOT NULL, url TEXT NOT NULL, PRIMARY KEY (id))")
        db.commit()
    except Exception as error:
        print(f"{bcolors.FAIL}{error}{bcolors.ENDC}")
    finally:
        print(f"{bcolors.OKGREEN}Database connected.{bcolors.ENDC}")

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

init_db()

if __name__ == "__main__":
    app.run()