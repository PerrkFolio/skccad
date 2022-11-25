import json

from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/p2p')
def p2p():
    return render_template("p2p.html")


# @app.route('/p2p/<string:crypto>/<string:fiat>/<int:volume>/<int:good_deals>', methods = ['GET'])
@app.route('/get_data/<string:crypto>', methods=['GET'])
def get_data(crypto):
    path = 'exchanges/json/okx_'+crypto+'.json'
    with open(path) as json_file:
        result = json.load(json_file)
        print(result)
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(host="136.243.0.97", debug=True)
