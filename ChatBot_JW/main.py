#NOTE: All words that need to be recognised in the JSON file should be lowercased.

import json
import re #正規運算式 (regular expression) 常用在對文件進行解析
import random_responses #隨機對話腳本
import requests #提出請求
import pymysql #與sql連動會用到
#import charts #資料庫圖表會用到


# Load/Store JSON data
def load_json(file):
    with open(file) as bot_responses: #開啟檔案，並傳給 bot_responses
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses) #以json的方式載入檔案
        	#with語句確保檔案可以於結尾確實關掉
    
response_data = load_json("bot.json")



def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower()) #以 pattern 為分隔島, 將母字串分開
    score_list = []
	
	  #Check all the responses
    for response in response_data:
        
        required_score = 0 #為必須條件，如果沒有符合必須條件則不會輸出該類別回應
        response_score = 0 #為加分條件，若一個輸入訊息符合多個類別的必須條件，則利用此分數來看該輸入跟哪個類別最相近
        required_words = response["required_words"] #取用.json腳本檔案的 required word 子類別

       	 #Check if there are any required words
        if required_words: #如果有需要的 required word
               for word in split_message: #遍歷輸入的訊息
                   if word in required_words: #如果使用者有輸入到 required word
                       required_score += 1 #加分
	      #Amount of required words should match the required score
        if required_score == len(required_words):
        	# print(required_score == len(required_words))
        	# Check each word the user has typed
            for word in split_message:
               	# If the word is in the response, add to the score
                	if word in response["user_input"]:
                    		response_score += 1
	
        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    	# Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    	# Check if input is empty
    if input_string == "":
        return "Please type something so we can chat :("
	
    	# If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_responses.random_string()

def start_gesture():
    print("Welcome to the chatbot service of Taiwan-India Talent Exchange website！")
    print("We provide the following functions：")
    print("--------------")
    print("【List Help Document】")
    print("You need to input: help\n")
    print("【List Personal Information】")
    print("You need to input: print personal information\n")
    print("【Find Best Plan】")
    print("You need to input: find best plan")
    print("--------------")

################################################################################
# 資料庫連線參數設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "password",
    "db": "test_schema",
    "charset": "utf8"
}

try:
    conn = pymysql.connect(**db_settings) # 建立Connection物件    
    with conn.cursor() as cursor: # 建立Cursor物件
        command = "SELECT * FROM charts"
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
        print(result)
except Exception as ex: #使用Python的try-except例外處理機制
    print(ex)



if __name__ == "__main__": #新增此行避免被引用時進入無窮迴圈
	start_gesture();
	while True:

	#	pass_score = 0
	#	#可藉由網路連線布林值check是否有斷線！
	#	if connect_website:

	#		pass_score += 1

		#可藉由登入授權布林值check是否有登入！
	#	if log_in:

	#		pass_score +=1

	#	if pass_score == 2:
			user_input = input("You: ")
			print("Bot: ", get_response(user_input))


