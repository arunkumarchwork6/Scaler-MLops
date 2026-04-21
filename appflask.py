from flask import Flask


app = Flask(__name__)


@app.route("/ping",methods = ['GET'])
def ping():
    return "I am working fine"

@app.route("/",methods = ['GET'])
def homeping():
    return "I am in home page"



if __name__ == '__main__':
    app.run(debug=True)


