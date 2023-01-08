from flask import Flask, render_template

app = Flask('main')
app.app_context()


@app.route("/ref")
@app.route("/link")
def get_page():
    return render_template("connect.html")