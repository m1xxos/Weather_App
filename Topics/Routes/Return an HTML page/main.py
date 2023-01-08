from flask import Flask, render_template

app = Flask('main')
app.app_context()


@app.route("/help")
def get_help():
    return render_template("help.html")


@app.route("/info")
def get_info():
    return render_template("info.html")
