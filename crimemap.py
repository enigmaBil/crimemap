import re
from dbhelper import DBHelper


from flask import Flask
from flask import render_template
from flask import request
import json
import datetime
import dateparser
import string


app = Flask(__name__)
DB = DBHelper()


categories = ['mugging', 'break-in', 'dancing']

def format_date(userdate):
        date = dateparser.parse(userdate)
        try:
            return datetime.datetime.strftime(date, "%d-%m-%y")
        except TypeError:
            return None
        
def convert(s):
      
    # initialization of string to ""
    new = ""
  
    # traverse in the string 
    for x in s:
        new += x 
  
    # return string 
    return new

def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    safeuserInput = list(filter(lambda x: x in whitelist, userinput))
    return convert(safeuserInput)

@app.route("/")
def index(error_message=None):
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print (e)
        crimes = None
    return render_template("index.html", crimes=crimes, categories=categories, error_message=error_message)


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
    if category not in categories:
        return index()
    date = request.form.get("date")
    # date = format_date(request.form.get("date"))
    # if not date:
        # return index("invalid date. Please use dd-mm-yyyy format")
    
    try: 
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return index()
    
    
    description = sanitize_string(request.form.get("description"))
    
    DB.add_crime(category, date, latitude, longitude, description)
    return index()


if __name__=='__main__':
    app.run(port=3001, debug=True)