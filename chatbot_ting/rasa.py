import json
import requests
import re
from database import *
url = "http://localhost:5005/model/parse"

def rasa(text):
    # 替換標點符號，避免影響AI判斷
    text = text.replace( 'C++', 'CPP').replace( 'c++', 'CPP')
    text = text.replace( 'C#', 'Csharp').replace( 'c#', 'Csharp')
    text = re.sub('[^a-zA-Z0-9]', ' ' , text)
    
    data = json.dumps({"text": text}, ensure_ascii=False).encode(encoding="utf-8")
    response = requests.post(url=url, data=data)
    response = json.loads(response.text)
    return response

def classify(intent):
    # 分類意圖與實體，整理並回傳

    if intent['intent']['name'] == 'find_projects':

        RequestPos = []
        RequestNeg = []
        nums = []
        most_confidence_num = (5,0.0)     #(num,confidence)#預設回傳5個projects

        if intent['entities']:
            entities = intent['entities']           
            for entity in entities:

                if entity['entity']=='num':
                    nums.append(int(entity['value']))
                    if most_confidence_num[1] < entity['confidence_entity'] and entity['confidence_entity'] > 0.75:
                        most_confidence_num = (int(entity['value']),entity['confidence_entity'])

                elif entity['entity']=='tags':

                    if entity['role']=='tags':
                        RequestPos.append((entity['value'],
                            entity['confidence_entity'],
                            entity['confidence_role']
                        ))

                    elif entity['role']=='neg_tags':
                        RequestNeg.append((entity['value'],
                            entity['confidence_entity'],
                            entity['confidence_role']
                        ))

        return {
            "intent":intent['intent']['name'],
            "confidence":intent['intent']['confidence'],
            "nums":nums,
            "most_confidence_num":most_confidence_num[0],
            "RequestPos":RequestPos,
            "RequestNeg":RequestNeg
        }

    else:
        return {
            "intent":intent['intent']['name'],
            "confidence":intent['intent']['confidence'],
        }



def query(result):


    RequestPos = result['RequestPos']
    RequestNeg = result['RequestNeg']

    num = result['most_confidence_num']   

    All_researches = all_researches()

    # 從RequestPos挑出有在運作的tag，放進RequestPos
    QueryPos = []
    for t in RequestPos:              
        if t[0].lower() in [ ar.lower() for ar in All_researches]:
            QueryPos.append(t[0])
        elif t[0].lower()=='cpp' and 'C++' in All_researches:
            QueryPos.append('C++')
        elif t[0].lower()=='csharp' and 'C#' in All_researches:
            QueryPos.append('C#')

    # 從RequestNeg挑出有在運作的tag，放進RequestNeg
    QueryNeg = []
    for nt in RequestNeg:              
        if nt[0].lower() in [ ar.lower() for ar in All_researches]:
            QueryNeg.append(nt[0])
        elif nt[0].lower()=='cpp' and 'C++' in All_researches:
            QueryNeg.append('C++')
        elif nt[0].lower()=='csharp' and 'C#' in All_researches:
            QueryNeg.append('C#')

    # 沒有符合需要tags的projects
    if QueryPos == [] and RequestPos != []: return "Sorry, We don't have the project you need."

    if len(QueryPos):     # 有說明需求
        projects = tagToProjects(tags=QueryPos,neg_tags=QueryNeg,limit=num)

    elif len(QueryNeg):   # 有說明不需要的部分
        projects = tagToProjects(tags=All_researches,neg_tags=QueryNeg,limit=num,order_by_match_num=False)

    else:                 # 沒說明，回傳最新的projects
        projects = latest_projects(limit=num)

    if projects == []: return "Sorry, We don't have the project you need."
    
    return htmlify(projects)    
    
    

def htmlify(dict):

    L = []

    if dict:

        num = 1 
        L.append("We recommend you the following Projects")
        num = 1 #輸出內容的序號，從1開始
        for project in dict:

            L.append(f"<div class=\"messages__item2 messages__item--visitor\">")
            L.append(f"<H3>PROJECT {str(num)} ：</H3>")
            L.append(f"Project Title：<a href=http://localhost:8080/#/projects/{str(project['id'])} target='_blank'>{str(project['project_title'])}</a><br>")
            L.append(f"Project Region： {str(project['researches'])}<br></div>")

            num = num + 1

        L.append(f'<a href="http://localhost:8080/#/projects" target="_blank">Click me to see more projects.</a>')

    else:
        L.append("Based on your needs, there are no matching projects.")

    return ''.join(L)


