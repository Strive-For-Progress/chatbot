from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re


def case1(input_text):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_text.lower()) #以 pattern 為分隔島, 將母字串分開
    need_language = [] #喜歡的語言
    notlike_language = [] #不喜歡的語言
    total_language = ["c++","c","python","c#","java"] #所有程式語言
    deny_language =["not","don\'t","doesn\'t"] #否定詞
    mode = 0 #0：之後碰到的語言都歸類於喜歡，1：之後碰到的語言都歸類於不喜歡

    #收集喜歡的語言以及不喜歡的語言
    for word in split_message:
        if(word in deny_language):
            mode = 1
            continue
        if(word in total_language & mode == 0):
            need_language.append(word)
            continue
        if(word in total_language & mode == 1):
            notlike_language.append(word)
            continue
    #SQL進行搜尋

    #處理結果

    #印出訊息

#while True:
    #input_text = input("You：")
total_language = ["c++","c","python","c#","java"]
print(total_language)
total_language.append("rrrr")
print(total_language)
word = "java"
if(word in total_language):
    print("yes");
else:
    print("no")

    #case1(input_text)


