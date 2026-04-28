from flask import Flask


app = Flask(__name__)


@app.route("/ping",methods = ['GET'])
def ping():
    return "I am working fine"

@app.route("/",methods = ['GET'])
def homeping():
    return "I am in home page test"



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


