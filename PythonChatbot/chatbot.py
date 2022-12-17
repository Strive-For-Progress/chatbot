from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re


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
        'maximum_similarity_threshold': 0.80
        }
    ],
    database_url='sqlite:///database.sqlite3'
)

trainer = ChatterBotCorpusTrainer(bot)
#先載入客服語料庫，告知使用者稍等一下載入時間。
trainer.train("english/service.yml")
response = bot.get_response("wait")
print(response)

#載入完整語料庫
trainer.train("english")

print("Welcome to the chatbot service of Taiwan-India Talent Exchange website！")
print("You can try to ask some questions.")
print("I will do my best to help you.")

def case1(input_text):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_text.lower()) #以 pattern 為分隔島, 將母字串分開
    need_language = [] #喜歡的語言
    notlike_language = [] #不喜歡的語言
    total_language = ["c","c++","c#","python","java"] #所有程式語言
    deny_language =["not","don\'t","doesn\'t"] #否定詞
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
    #SQL進行搜尋

    #處理結果

    #印出訊息
    print(need_language)
    print(notlike_language)



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
