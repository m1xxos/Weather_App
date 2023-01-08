from flask import Flask, Response

app = Flask('main')


@app.route('/data/main_info')
def view_func1():
    return Response("<h1>Hello there, it's me — my own worst enemy!</h1>", status=200)


@app.route('/the_wall')
def view_func2():
    return Response("<h1>Welkommen!</h1>", status=200)