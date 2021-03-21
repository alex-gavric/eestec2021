from setup import *
from functions import *
from flask import Flask, request

app = Flask(__name__)
app.debug = True

@app.route('/list', methods=['GET'])
def GetListRoute():
    return GetList()

@app.route('/search', methods=['POST'])
def SearchRoute():
    inputString = str(request.form.get("queryString"))
    print("is: " + inputString)
    return SearchIP(inputString)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    