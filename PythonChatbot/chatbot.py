from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

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

while True:
    
    response = bot.get_response(input("You："))
    #需要特別轉字串才可以判別
    str_response = str(response)
    print("Bot：", end='')

    if(str_response == "SPECIALCASE1"):
        #可以做特別計算
        print("It's special case 1.")
    else:
        print(str_response)
