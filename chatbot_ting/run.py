from app import create_app, db
from flask import Flask, render_template, request, jsonify
from rasa import *
from chat import *

app = create_app('production')

@app.route("/",methods=["GET"])
def index_get():
    return render_template("index.html")


@app.route("/predict",methods=["POST"])
def predict():

    text = request.get_json().get("message")
    
    token = request.get_json().get("isLogin")

    result = rasa(text)
    intent = classify(result)

    if intent['confidence'] > 0.9:

        if(intent['intent']) == 'find_projects':

            if(token == None):      # Not login
                    message = 'Please login first.'

            if len(intent['nums']) in range(0,2):

                if intent['most_confidence_num']:
                    message = query(intent)

                else:       # ask for 0 projects
                    message = 'Here you are.'

            else:
                message = 'Too much numbers'
        else:
            message = chat(intent['intent'])


    else:
        message = "Sorry, I don't know what you say."


    message = {"answer": str(message)}
    return jsonify(message)


if __name__ == "__main__":
    app.run()


