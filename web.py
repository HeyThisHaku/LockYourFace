from flask import Flask, render_template, Response, redirect, request
import core

# training
core.detect_face()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/lock/', methods=['POST'])
def lock():
    try:
        if request.method == 'POST':
            path = request.form.get('path')
            return Response(core.live('lock',path), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(e)


@app.route('/unlock/', methods=['POST'])
def unlock():
    try:
        if request.method == 'POST':
            path = request.form.get('path')
            return Response(core.live('unlock',path), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run()
