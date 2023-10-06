import jieba
import jieba.posseg as pseg
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer

TEST = True

class prompt:
    def __init__(self):
        if not TEST:
            from modelAPI.Baidu.ERNIE_Bot import ERNIE_Bot
            from modelAPI.Baidu.ChatGLM import ChatGLM
            from modelAPI.Baidu.Llma_2 import Llma_2

            
            self.user_input = ""

            self.llma_2 = Llma_2()
            self.ernie_bot = ERNIE_Bot()
            self.chatglm = ChatGLM()
            self.bot_name_list = ["llma_2", "ernie_bot", "chatglm"]
            self.bot_dict = {"llma_2":self.llma_2, "ernie_bot":self.ernie_bot, "chatglm":self.chatglm}
        else:

            self.user_input = ["长沙有几所985大学呢？"]
        
        
    
    def calculate_tfidf(self,n_keywords=3):
        # 将句子分成单词
        sentence = self.user_input
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform(sentence)
        feature_names = vectorizer.get_feature_names_out()
        
        # 获取每个文档的 top n 关键词
        keywords = []
        for vector in vectors:
            indices = vector.indices
            data = vector.data
            sorted_indices = [index for _, index in sorted(zip(data, indices), reverse=True)]
            keywords.append([feature_names[i] for i in sorted_indices[:n_keywords]])
    
        return keywords
    
p = prompt()
print(p.calculate_tfidf())
