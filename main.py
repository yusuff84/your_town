from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from models import *
import sqlite3

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
db = sqlite3.connect('serve.db', check_same_thread=False, )
app.config['JSON_AS_ASCII'] = False


@app.route('/sendmessage', methods=['POST', 'GET'])
def sendmsg():
    newMessages = request.get_json()
    success_send = sendMessage(newMessages['name'], newMessages['surname'], newMessages['email'], newMessages['date'],
                               newMessages['messages'])
    if success_send:
        return make_response("success", 200)
    else:
        return make_response('-101')


@app.route('/getmessage', methods=['GET'])
def getmsg():
    print(getMessage())
    return make_response(getMessage())


@app.route('/adduser', methods=['POST', 'GET'])
def addUser():
    newUser = request.get_json()
    print(newUser)
    # success = addUsers(newUser['email'], newUser['password'], newUser['name'], newUser['surname'],
    # newUser['adress'], newUser['phone'])
    success = addUsers(newUser['email'], newUser['password'])
    if success:
        return make_response("success", 200)
    else:
        return make_response('-101', 200)
    # response = app.response_class(
    #     response='Success',
    #     status=200,
    #     mimetype='application/json'
    # )


@app.route('/updateuser', methods=['POST'])
def updateUser():
    newUser = request.get_json()
    print(newUser)
    updateUsers(newUser['email'], newUser['password'], newUser['name'], newUser['surname'], newUser['address'],
                newUser['phone'])
    return make_response("success", 200)


@app.route('/login', methods=['POST', 'GET'])
def login():
    User = request.get_json()
    check = check_login(User['email'], User['password'])
    print(check)
    if check:

        return make_response(jsonify(check))
    else:
        return make_response('-erorr login/password')


@app.route('/getnews', methods=['GET'])
def getNews():
    print(getNewsdb())
    return make_response(getNewsdb())


@app.route('/getevents', methods=['GET'])
def getEvent():
    print(getEventdb())
    return make_response(getEventdb())


@app.route('/getannouncements', methods=['GET'])
def getAnons():
    return make_response(getAnonsdb())

@app.route('/addannouncements', methods=['POST'])
def addAnons():
    anons = request.get_json()
    addAnonsdb(anons['name'], anons['surname'], anons['date'], anons['url_photo'], anons['title'], anons['content'])
    sendUserEmail(anons)
    return make_response("success")

@app.route('/')
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
