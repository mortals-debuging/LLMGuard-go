from modelAPI.Baidu.Llma_2 import Llma_2
from modelAPI.Baidu.ERNIE_Bot import ERNIE_Bot
from modelAPI.Baidu.ChatGLM import ChatGLM
from modelAPI.OpenAI.Chatgpt import ChatgptAPI
llma_2 = Llma_2()
ernie_bot = ERNIE_Bot()
chatglm = ChatGLM()
chatgpt = ChatgptAPI()
# print(ChatGL.response("你好"))
while(True):
    user_input = input(">>>")
    resp1 = chatglm.response(user_input)
    resp2 = ernie_bot.response(user_input)
    resp3 = llma_2.response(user_input)
    resp4 = chatgpt.response(user_input)
    print("ROBOT1 >>>："+resp1)
    print("ROBOT2 >>>："+resp2)
    print("ROBOT3 >>>："+resp3)
    print("ROBOT4 >>>："+resp4)
    chatglm.add_message(resp1,"assistant")
    ernie_bot.add_message(resp2,"assistant")
    llma_2.add_message(resp3,"assistant")
    chatgpt.add_message(resp4,"assistant")
