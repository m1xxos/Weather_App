from flask import Flask, make_response

app = Flask('main')


@app.route('/<data>')
def main_view(data):
    return make_response(data, 204)
