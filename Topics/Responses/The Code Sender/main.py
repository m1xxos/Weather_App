from flask import Flask, jsonify

app = Flask('main')
app.app_context()


@app.route('/<data>')
def response_maker(data):
    text, status_code = data.split(';')

    response = jsonify({"code": status_code, "message": text})
    return response
