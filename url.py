#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, render_template, abort, url_for
import mysql.connector
from dotenv import load_dotenv
from urllib.parse import urlparse
import random
import string
load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_DATABASE")
)

c = db.cursor()

@app.route("/", methods = ["GET", "POST"])
def page():
    if request.method == "POST":
        try:
            url = request.form["url"]
        except KeyError:
            abort(400)
        if validate_url(url):
            slug = save_db(url)
            return render_template("done.html", Title = "Short URL", Slug = os.getenv("BASE_URL") + "/s/" + slug)
        return render_template("error.html", Title = "Error")
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
Validates given url.
"""
def validate_url(url):
    try:
        if url.find(os.getenv("BASE_URL")) > -1:
            return False
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

"""
Saves given url in database but return slug if already stored.
"""
def save_db(url):
    c.execute("SELECT slug FROM urls WHERE url = %(url)s;", { "url": url })
    slug = c.fetchone()
    if slug is not None:
        return slug[0]
    new_slug = get_unique_slug()
    c.execute("INSERT INTO urls (id, slug, url) VALUES (null, %(slug)s, %(url)s);", { "slug": new_slug, "url": url })
    db.commit()
    return new_slug


"""
Generate unique slug.
"""
def get_unique_slug():
    slug = get_random_string()
    while not isUniqueSlug(slug):
        slug = get_random_string()
    return slug

"""
Returns boolean if random string is already stored as slug.
"""
def isUniqueSlug(slug):
    c.execute("SELECT * FROM urls WHERE slug = %(slug)s;", { "slug": slug })
    return c.fetchone() is None


"""
Get random 5 char with number string.
"""
def get_random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

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
