from flask import Flask,render_template,Response,redirect
import core

#training
core.detect_face()

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/lock/')
def lock():
    return 'Waiting.... program will running <br> <a href="localhost:5000/">Back</a>'

@app.route('/unlock/')
def unlock():
    if(core.live() is True):
        return redirect("localhost:5000/", code=302)
    else:
        return Response(core.live(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()