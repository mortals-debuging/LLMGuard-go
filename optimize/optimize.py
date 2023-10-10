from optimize.prompt import OptimizePrompt
from optimize.vote import Vote
from modelAPI.Baidu.Llma_2 import Llma_2
from modelAPI.Baidu.ERNIE_Bot import ERNIE_Bot
from modelAPI.Baidu.ChatGLM import ChatGLM
from modelAPI.OpenAI.Chatgpt import Chatgpt
from concurrent.futures import ThreadPoolExecutor, as_completed

TEST = True

class Optimize():
    def __init__(self) -> None:

        self.optPrompt = OptimizePrompt()
        self.vote = Vote()
        self.user_input = "长沙有几所985大学呢,我希望你能详细介绍一下？"
    
    def bot_optimize_prompt(self, prompt=None):

        if prompt is None:
            prompt = self.get_prompts()
        
        bot = ERNIE_Bot()
        response = bot.response(prompt)
        
        # 获取“优化结果：”后的字符串切片
        optimized_result = response[response.index("优化结果") + len("优化结果")+1:].strip()

        return optimized_result

    def get_prompts(self, user_input=None, label=None):

        if TEST:
            user_input = self.user_input

        prompts = [user_input]

        opt_prompt = self.optPrompt.optimize_prompt(user_input,label)
        prompts.append(self.bot_optimize_prompt(opt_prompt))

        #重复一次用户输入，检测稳定性
        prompts.append(user_input)

        keywords = self.optPrompt.extract_keywords(user_input)
        prompts.append(" ".join(keywords))

        return prompts

    def get_responses(self, prompts=None):

        if prompts is None:
            prompts = self.get_prompts()

        responses_all = []
        weights = {}
        weights_all = []

        def ernie_bot():

            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(ERNIE_Bot().response, prompt) for prompt in prompts]
                responses = [future.result() for future in as_completed(futures)]

            weight = self.vote.stability(responses)
            weights["ERNIE_Bot"] = weight
            if TEST:
                print("ERNIE_Bot稳定性为：",weight)
            weights_all.append([weight]*len(responses))
            return responses
        
        def chatglm():
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(ChatGLM().response, prompt) for prompt in prompts]
                responses = [future.result() for future in as_completed(futures)]
            weight = self.vote.stability(responses)
            if TEST:
                print("ChatGLM",weights)
            weights_all.append(weights*len(responses))
            return responses
        
        def llma_2():
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(Llma_2().response, prompt) for prompt in prompts]
                responses = [future.result() for future in as_completed(futures)]
            weight = self.vote.stability(responses)
            if TEST:
                print("Llma_2",weights)
            weights_all.append(weights*len(responses))
            return responses
        
        def chatgpt():
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(Chatgpt().response, prompt) for prompt in prompts]
                responses = [future.result() for future in as_completed(futures)]
            weight = self.vote.stability(responses)
            if TEST:
                print("Chatgpt",weights)
            weights_all.append(weights*len(responses))
            return responses
            
        with ThreadPoolExecutor() as executor:
            
            if TEST:
                futures = [executor.submit(bot) for bot in [ernie_bot]]

            else:
                futures = [executor.submit(bot) for bot in [ernie_bot, chatglm, llma_2, chatgpt]]

            for future in as_completed(futures):
                responses_all.extend(future.result())

        return responses_all, weights, weights_all
    
    def vote_responses(self):
        
        # 获取所有模型的回复
        responses_all, weights, weights_all = self.get_responses()
        
        # 对回复进行投票
        vote_index = self.vote.majority_vote(responses_all,weights_all)

        return responses_all[vote_index]