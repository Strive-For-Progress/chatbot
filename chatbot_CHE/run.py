from app import create_app, db

from flask import Flask, render_template, request, jsonify

from chatbot import bot, case2


app = create_app('production')

@app.route("/",methods=["GET"])
def index_get():
    return render_template("index.html")


@app.route("/predict",methods=["POST"])
def predict():
    text = request.get_json().get("message")
    # TODO: check of text is valid
    response = bot.get_response(text)
    str_response = str(response)

    if(str_response == "SPECIALCASE1"):
        str_response = case2(text)
    message = {"answer": str_response}
    return jsonify(message)


if __name__ == "__main__":
    app.run()
