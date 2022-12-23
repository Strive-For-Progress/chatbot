import json
import requests
import re
url = "http://localhost:5005/model/parse"

if __name__ == "__main__":

    connect = False
    if input("\nConnect to mysql.cs.ccu.edu.tw? Y/[N] ").lower() in ['y','yes','1'] : 
        from database import *
        connect = True

    print("========================================")
    while 1:
        text = input("input:     ")
        text = text.replace( 'C++', 'CPP').replace( 'c++', 'CPP')
        text = text.replace( 'C#', 'Csharp').replace( 'c#', 'Csharp')
        text = re.sub('[^a-zA-Z0-9_]', ' ' , text)
        
        
    
        data = json.dumps({"text": text}, ensure_ascii=False).encode(encoding="utf-8")
        response = requests.post(url=url, data=data)
        response = json.loads(response.text)
        # print(response)


        print('\n%-10s'%'text:',response['text'])
        print('%-10s' %"intent: ","%-15s"%response['intent']['name'],"  Confidence:  ", response['intent']['confidence'])
        if response['intent']['name'] == 'find_projects':
            RequestPos = []
            RequestNeg = []
            num = []

            if response['entities']:
                entities = response['entities']           
                for entity in entities:

                    if entity['entity']=='num':
                        num.append(entity['value'])

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
                if num:
                    print('%-10s'%"Num:",num[0])
                if RequestPos:
                    print("RequestPos:")
                    for t in RequestPos:
                        print('%10s'%'','%-8s'%t[0],'   entity: ','%-5f'%t[1],'   role: ','%-5f'%t[2])
                if RequestNeg:
                    print("RequestNeg:")
                    for t in RequestNeg:
                        print('%10s'%'','%-8s'%t[0],'   entity: ','%-5f'%t[1],'   role: ','%-5f'%t[2])

            if connect:
                print("")
                print("RequestPos:    ",[t[0] for t in RequestPos])
                print("RequestNeg:    ",[nt[0] for nt in RequestNeg])
                All_researches = all_researches()
                print('\n%-15s'%"All_researches:", All_researches)
                QueryPos = []
                QueryNeg = []
                for t in RequestPos:              
                    if t[0].lower() in [ ar.lower() for ar in All_researches]:
                        QueryPos.append(t[0])
                    elif t[0].lower()=='cpp':
                        QueryPos.append('C++')
                    # elif t[0].lower()=='csharp':
                    #     QueryPos.append('C#')

                for nt in RequestNeg:              
                    if nt[0].lower() in [ ar.lower() for ar in All_researches]:
                        QueryNeg.append(nt[0])
                    elif nt[0].lower()=='cpp':
                        QueryNeg.append('C++')
                    # elif t[0].lower()=='csharp':
                    #     tags.append('C#')

                print('%-15s'%"QueryPos:", QueryPos)
                print('%-15s'%"QueryNeg:", QueryNeg)
                
                if num:
                    print('%-15s'%"Num:", num[0])
                    limit = int(num[0])
                else:
                    limit = 5
                for p in tagToProjects(tags=QueryPos,neg_tags=QueryNeg,limit=limit,user_id=-1):
                    print(p)        


        print("========================================")
            


# We don't have the project you need.
# We recommend fowlloing projects:
