import random
def chat_greet():
    return random.choice([
    "hey",
    "hello",
    "hi",
    "hello there",
    "How are you doing?",
    "Hi, How is it going?",
    "moin",
    "hey there",
    "how are you",
    "Nice to meet you.",
    "Hi, nice to meet you.",
    "It is a pleasure to meet you."
    ])

def chat_goodbye():
    return random.choice([
        "cu",
        "cee you later",
        "bye",
        "have a nice day",
        "see you around",
        "bye bye",
        "see you later",
        "see you"
    ])

def chat_thank():
    return random.choice([
        "It's my pleasure",
        "You're welcome",
        "My pleasure"
    ])

def chat_broken():
    return random.choice([
        "Sorry, I'm not feeling well, I might need to see a engineer.",
        "I'm a little dizzy, maybe I need a fix.",
        "My body seems a little weird today, I'm sorry, I'll report for repairs on my own."
    ])

def chat(intent):
    if   intent == 'greet':
        return chat_greet()

    elif intent == 'goodbye':
        return chat_goodbye()

    elif intent == 'thank':
        return chat_thank()

    elif intent == 'broken':
        return chat_broken()

    
    return "Sorry, I don't know what you say"
    

