from app import create_app, db
from flask import Flask, render_template, request, jsonify
from chat import get_response
from database import *

app = create_app('production')

@app.route("/",methods=["GET"])
def index_get():
    return render_template("base.html")

@app.route("/predict",methods=["POST"])
def predict():
   
    # token = request.get_json().get("isLogin")
    # if(token == None):
    #     return jsonify({"answer": 'pls login' }) 
    
    text = request.get_json().get("message")
    if(text == 'case1'):
        projects = user_prefer_project(user_id=7)
        return jsonify({"answer": "case1" , "projects":projects})
    if(text == 'case2'):
        projects = all_projects()
        return jsonify({"answer": "case2" , "projects":projects})
    if(str(text).startswith('case3')):
        tags=[]
        for tag in all_researches():
            if tag in text:
                tags.append(tag)
        projects = tagToProjects(tags=tags,user_id=-1,limit=-1) 
        #若填入usr則不考慮usr是PI、COPI的project    #limit<0時不限制數量
        return jsonify({"answer": "case3" , "projects":projects})
    if(text == 'case4'):
        researches = all_researches()
        return jsonify({"answer": "case4" , "researches":researches})


    response = get_response(text)
    message = {"answer":response}
    return jsonify(message)

if __name__ == "__main__":
    app.run()
