import jieba
import jieba.analyse
import jieba.posseg as pseg
import re

class OptimizePrompt:
    def __init__(self):
            
        self.user_input = "长沙有几所985大学呢,我希望你能详细介绍一下？"
        self.label = ["生活常识","志愿填报","学校信息","其他"]

        self.prompt = "你现在的任务是优化问题prompt。你首先在（"+str(self.label)+"）中选择分类。格式为：分类结果： 优化结果：。这个Prompt是：\"" + self.user_input +"\""
        jieba.load_userdict("votePart/PromptText/specialword.txt")
    
    def extract_keywords(self, text,n=3):

        #jieba已经加载了词典
        keywords = jieba.analyse.extract_tags(text, topK=n)
        print("/".join(keywords))
        return keywords

    
    def extract_keywords_with_pos(self, text, keywords):

        # 直接对整个文本进行词性标注
        words_with_pos = [(word, flag) for word, flag in pseg.cut(text) if word in keywords]

        return words_with_pos

    def optimize_prompt(self, user_input=None, label=None):
        if user_input is None:
            user_input = self.user_input
        if label is None:
            label = self.label

        # 提取关键词
        keywords = self.extract_keywords(user_input)

        # 提取实体
        entities = self.extract_keywords_with_pos(user_input,keywords)
        print(entities)
        
        # 生成优化后的prompt
        prompt = "你现在的任务是优化问题prompt。你首先在（"+str(label)+"）中选择分类。格式为：分类结果： 优化结果：。这个Prompt是：\"" + user_input +"\""
        for entity in entities:
            entity = entity[0]
            prompt = prompt.replace(entity, "["+entity+"]")
            
        return prompt