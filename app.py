# ROUTE LIST:
# index - main interface
# accounts - edit accounts
# items - edit items
# settings - edit settings
# admin - admin menu
# api - api stuff

from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/accounts")
def show_accounts():
    # NOT IMPLEMENTED
    return "<h1>This page is not implemented.</h1><h2>Accounts Page</h2>"

@app.route("/items")
def show_items():
    # NOT IMPLEMENTED
    return "<h1>This page is not implemented.</h1><h2>Items Page</h2>"

@app.route("/item/<int:id>")
def show_item(id):
    # NOT IMPLEMENTED
    return f"<h1>This page is not implemented.</h1><h2>The ID of the item you are trying to get is {id}</h2>"

@app.route("/settings")
def settings():
    # NOT IMPLEMENTED
    return "<h1>This page is not implemented.</h1><h2>Settings Page</h2>"

@app.route("/admin")
def admin():
    # NOT IMPLEMENTED
    return "<h1>This page is not implemented.</h1><h2>Admin Page</h2>"