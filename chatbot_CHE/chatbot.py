from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import pymysql

db = pymysql.connect(host='mysql.cs.ccu.edu.tw',
                    user='xbt109u',
                    password='xbt109u',
                    database='xbt109u_appdb')

#import sys
bot = ChatBot(
    'Built-in adapters',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        #'my_adapter.MyLogicAdapter',
        'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter',
        #'chatterbot.logic.BestMatch',
        'chatterbot.logic.UnitConversion',
        #'chatterbot.logic.ClosestMeaningAdapter'
        {
        #設定當可信度低於一定數值時，回覆預設對話
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I would be able to provide a better answer if you could be more specific.',
        'maximum_similarity_threshold': 0.90
        }
    ],
    database_url='sqlite:///database.sqlite3',
    read_only="true"
)

def all_projects(live = True,limit=5):
    # 列出所有project、project的id、title、researches
    # (live=True:不包含過期(copi_end_time))，反之包含
    # limit不填預設5

    if live: live_text = "AND NOW() < sp.apply_copi_end_date "
    else: live_text = ""

    if(limit < 0): limit = 5

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = (
            "SELECT sp.id, sp.project_title "
                ", GROUP_CONCAT(c.name ORDER BY c.id) AS researches "
            "FROM specific_periods sp "
            "JOIN specific_period_researches spr ON spr.specific_period_id = sp.id "
            "JOIN researches c ON c.id = spr.research_id "
            f"{live_text}"
            "GROUP BY sp.id "
            "ORDER BY sp.id "
            f"LIMIT 0,{limit} "
        )

    cursor.execute(sql)
    results = cursor.fetchall()

    return results

def tagToProjects(tags=[],neg_tags=[],user_id=-1,live=True,limit=5):
    # 依據tags內容(match越多越優先)，列出user_id非PI、COPI的project
    # 不填user則直接依tags計算 
    # tags不填 回傳[] , neg_tags不填 依tags計算
    # limit不填預設5

    if(len(tags) == 0): return []
    else: tags_text =  '"' + '","'.join(tags) + '"'

    if(limit <= 0): limit = 5 

    if live: live_text = "AND NOW() < sp.apply_copi_end_date "
    else: live_text = ""

    if(len(neg_tags) == 0): neg_tags_text = ""
    else:
        neg_tags_text = (
            "WHERE "
            "match_table.id NOT IN ( "
                "SELECT sp.id "
                "FROM specific_periods sp "
                "JOIN researches r "
                "JOIN specific_period_researches spr "
                "WHERE "
        ) 
        neg_tags_text += 'r.name IN ("' + '","'.join(neg_tags) + '") '        
        neg_tags_text += (
                    "AND r.id = spr.research_id AND spr.specific_period_id = sp.id "
                    "GROUP BY sp.id "
            ") "
        )

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)    
    sql=(
        "SELECT sp.id, sp.project_title, GROUP_CONCAT(r.name ORDER BY r.id ASC) AS researches "
        "FROM specific_periods sp "
        "JOIN ( "
                "SELECT sp.id, COUNT(distinct r.id) AS match_num "
                "FROM researches r "
                "INNER JOIN specific_period_researches spr "
                "INNER JOIN specific_periods sp "
                "INNER JOIN users u "
                
                "WHERE "
                    f"r.name IN ({tags_text}) "
                    "AND r.id = spr.research_id AND spr.specific_period_id = sp.id "
                    f"{live_text}"
                    "AND u.id = sp.user_id "
                    f"AND u.id != {user_id} AND {user_id} NOT IN (SELECT user_id FROM COPI_project CO WHERE CO.specific_period_id = sp.id) "
                
                "GROUP BY sp.id " 
                ") match_table ON match_table.id = sp.id "
        "JOIN specific_period_researches spr ON spr.specific_period_id = sp.id "
        "JOIN researches r ON spr.research_id = r.id "
        f"{neg_tags_text}"
        "GROUP BY sp.id "
        "ORDER BY match_num DESC "
        f"LIMIT 0, {limit} "
    )

    cursor.execute(sql)
    results = cursor.fetchall()

    return results

def case1(input_text):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_text.lower()) #以 pattern 為分隔島, 將母字串分開
    need_language = [] #喜歡的語言
    notlike_language = [] #不喜歡的語言
    total_language = ["c","c++","c#","python","java","javascript","php","html","css","sql","ai","web","dl","deep learning"] #所有程式語言
    deny_language =["not","don\'t","doesn\'t","can\'t","no","never","without","non","unlike","unwilling","hate","dislike"] #否定詞
    mode = 0 #0：之後碰到的語言都歸類於喜歡，1：之後碰到的語言都歸類於不喜歡

    #收集喜歡的語言以及不喜歡的語言
    for word in split_message:
        if(word in deny_language):
            mode = 1
            continue
        if(word in total_language):
            if mode==0:
                need_language.append(word)
            elif mode==1:
                notlike_language.append(word)

    if (need_language==[]) and (notlike_language==[]):
        #沒有說偏好，就根據個人資訊去尋求推薦
        print("We will search by your info.")
    else:
        #SQL進行搜尋
        target_researchs = tagToProjects(need_language,notlike_language,user_id=-1,live=True,limit=5)
        result = []

        if target_researchs:
            #印出訊息
            num = 1 #輸出內容的序號，從1開始
            print("We recommend you the following research：")
            for research in target_researchs:
                print("RESEARCH", num,"：")
                print("Research Title：",research["project_title"])
                print("Research Region：",research["researches"])
                print("More Information：http://localhost:8080/#/projects/",research["id"],sep='')
                print("")
                num = num + 1
        else:
            print("Based on your needs, there are no matching research.")

def case2(input_text): #for website
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_text.lower()) #以 pattern 為分隔島, 將母字串分開
    need_language = [] #喜歡的語言
    notlike_language = [] #不喜歡的語言
    total_language = ["c","c++","c#","python","java","javascript","php","html","css","sql","ai","web","dl","deep learning"] #所有程式語言
    deny_language =["not","don\'t","doesn\'t","can\'t","no","never","without","non","unlike","unwilling","hate","dislike"] #否定詞
    mode = 0 #0：之後碰到的語言都歸類於喜歡，1：之後碰到的語言都歸類於不喜歡
    L = []
    #收集喜歡的語言以及不喜歡的語言
    for word in split_message:
        if(word in deny_language):
            mode = 1
            continue
        if(word in total_language):
            if mode==0:
                need_language.append(word)
            elif mode==1:
                notlike_language.append(word)

    if (need_language==[]) and (notlike_language==[]):
        #沒有說偏好，就根據個人資訊去尋求推薦
        L.append("We will search by your info.")
        #print("We will search by your info.")
    else:
        #SQL進行搜尋
        target_researchs = tagToProjects(need_language,notlike_language,user_id=-1,live=True,limit=5)
        if target_researchs:
            #印出訊息
            num = 1 #輸出內容的序號，從1開始
            L.append("We recommend you the following research：")
            L.append("")
            #print("We recommend you the following research：")
            for research in target_researchs:
                str1 = "RESEARCH" + str(num) + "："
                L.append(str1)
                str1 = "Research Title：" + str(research["project_title"])
                L.append(str1)
                str1 = "Research Region：" + str(research["researches"])
                L.append(str1)
                str1 = "More Information：<a href=\"http://localhost:8080/#/projects/" + str(research["id"]) + "\" target=\"_blank\">" + str(research["project_title"]) + "</a>"
                L.append(str1)
                str1 = ""
                L.append(str1)
                #print("RESEARCH", num,"：")
                #print("Research Title：",research["project_title"])
                #print("Research Region：",research["researches"])
                #print("More Information：http://localhost:8080/#/projects/",research["id"],sep='')
                #print("")
                num = num + 1
        else:
            L.append("Based on your needs, there are no matching research.")
            #print("Based on your needs, there are no matching research.")
    return '<br>'.join(L)


##################################################################
trainer = ChatterBotCorpusTrainer(bot)
#先載入客服語料庫，告知使用者稍等一下載入時間。
trainer.train("english/service.yml")
response = bot.get_response("wait")
print(response)

#載入完整語料庫
trainer.train("english")



if __name__ == "__main__": #新增此行避免被引用時進入無窮迴圈
    print("Welcome to the chatbot service of Taiwan-India Talent Exchange website！")
    print("You can try to ask some questions.")
    print("I will do my best to help you.")

    while True:
        input_text = input("You：")
        response = bot.get_response(input_text)
        
        #需要特別轉字串才可以判別
        str_response = str(response)

        print("Bot：", end='')

        if(str_response == "SPECIALCASE1"):
            #可以做特別計算
            print("It's special case 1.")
            case1(input_text)
        else:
            print(str_response)
         
