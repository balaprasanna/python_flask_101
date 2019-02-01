from flask import Flask, Response, request
from datetime import datetime
import json

app = Flask(__name__)

historylist = []

operator_dct = {
    "add": "+",
    "sub": "-",
    "mul": "*",
    "div": "/",
}

@app.route("/")
def index():
    return "Hello world"

@app.route("/time")
def time():
    return f"<h1> {str(datetime.now())} <h1>"

@app.route("/api/v1/calculate")
def calculate():

    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    operator = request.args.get("operator")
    ops = operator_dct[operator]
    result = eval(f"a {ops} b")
    resp =   {
                "status" : True,
                "result" : {
                "ops" : f"{a} {ops} {b}",
                "result" : result
                }
    }

    historylist.append(resp)
    resp = json.dumps(resp)
    return Response( resp , content_type="application/json")


@app.route("/api/v1/history")
def history():
    
    if request.args.get("limit"):
        limit = int(request.args.get("limit"))
    else:
        limit = 1
    resp = json.dumps(historylist[ -limit: ] )
    return Response(  resp, content_type="application/json"  )

app.run(host='0.0.0.0', port=5000, debug=True)
