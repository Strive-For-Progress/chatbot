from app import create_app, db

from flask import Flask, render_template, request, jsonify

from chat import get_response


app = create_app('production')

@app.route("/",methods=["GET"])
def index_get():
    return render_template("index.html")


@app.route("/predict",methods=["POST"])
def predict():
    text = request.get_json().get("message")
    # TODO: check of text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run()
