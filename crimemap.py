import re
from dbhelper import DBHelper


from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def index():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print (e)
        data = None
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(e)
    return index()


@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return index()

@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_crime(category, date, latitude, longitude, description)
    return index()


if __name__=='__main__':
    app.run(port=3001, debug=True)