import torch
import math
import statistics
from sentence_transformers import SentenceTransformer, util

class Vote:
    def __init__(self):
        self.model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    def cosine_similarity(self,answers):
        # 初始化Sentence-BERT模型
        model = self.model
        
        # 对回答进行编码
        embeddings = model.encode(answers)

        # 计算所有输出之间的余弦相似度
        cosine_sims = util.pytorch_cos_sim(embeddings, embeddings)

        return cosine_sims

    def stability(self,answers):
        cosine_sims  = self.cosine_similarity(answers)
        # 将矩阵的下三角部分置为0
        cosine_sims = torch.triu(cosine_sims, diagonal=1)
        # 找到非0元素的索引
        non_zero_indices = torch.nonzero(cosine_sims)

        # 使用索引从矩阵中提取非0元素
        non_zero_values = cosine_sims[non_zero_indices[:, 0], non_zero_indices[:, 1]]

        # 计算均值和方差
        mean = torch.mean(non_zero_values).item()
        std = torch.std(non_zero_values).item()

        # 计算稳定性
        stability = math.exp(-std / mean)
        print("稳定性为：", stability)
        return stability
    
    def majority_vote(self,answers,weights=None):
        
        if weights is None:
            weights = [1] * len(answers)

        # 将权重转换为张量
        weights_tensor = torch.tensor(weights)
        # 计算weights的转置
        weights_transpose_tensor = weights_tensor.unsqueeze(1).transpose(0, 1)

        cosine_sims  = self.cosine_similarity(answers)

        # 将矩阵中的元素与权重相乘
        cosine_sims = cosine_sims * weights_tensor * weights_transpose_tensor

        # 扁平化矩阵
        flattened = cosine_sims.flatten()

        # 对元素进行排序
        sorted_tensor, _ = torch.sort(flattened)
        # 计算四分位数
        quartiles = statistics.quantiles(sorted_tensor, n=4)
        # 取四分位数的前三分之一部分
        three_quarters = quartiles[2]

        # 将矩阵中小于四分位数的元素置为0
        cosine_sims = torch.where(cosine_sims < three_quarters, torch.zeros_like(cosine_sims), cosine_sims)
        #计算每一行的和
        row_sums = torch.sum(cosine_sims, dim=1)
        # 找到最大值的坐标
        max_indices = torch.where(row_sums == torch.max(row_sums))
        print("最大值的坐标为：", max_indices[0].item())
        return max_indices[0].item()

answers = [
    "长沙是湖南省的省会城市，拥有多所985高校。以下是长沙的985高校名单：1. 中南大学2. 湖南大学3. 国防科技大学4. 湖南师范大学5. 湖南科技大学6. 长沙理工大学7. 湖南工业大学8. 湖南农业大学9. 中南林业科技大学10. 湖南中医药大学需要注意的，这个名单并不是固定不变的。由于各种原因，一些高校可能会在未来被认定为985高校，或者一些高校可能会被降格为985高校。此外，不同年份的985名单可能会有所不同。",
    "长沙有**三所**985大学，分别是国防科技大学、中南大学、湖南大学。",
    "以下是几所位于长沙的 985 大学：1. 湖南大学：位于长沙市岳麓区，是一所以理工为主、文、法、经、管、教育、医、艺术等多学科协调发展，综合性研究型大学。2. 中南大学：位于长沙市岳麓区，是一所以冶金、材料、化学、物理、生命科学、电子、信息、机械等为主要特色的全国重点大学。3. 国防科技大学：位于长沙市岳麓区，是一所全国重点大学，主要为军队培养高级军事人才和高水平科研人才。4. 湖南师范大学：位于长沙市岳麓区，是一所以教育为主要学科的综合性师范大学，涵盖理、文、史、法、管、教育、理、工等多个学科领域。5. 湖南农业大学：位于长沙市岳麓区，是一所以农业科学为主要特色的全国重点大学，涵盖农学、工学、理学、经济学、管理学等多个学科领域。以上是长沙地区的几所 985 大学，它们都是中国高等教育领域的重要代表，拥有着较高的学术声誉和优秀的教育资源。",
    "根据公开信息，长沙市有**三所**985大学，分别是国防科技大学、中南大学和湖南大学。",
    "长沙是湖南省的省会城市，有多所知名高等教育机构。以下是长沙的985大学：1. 湖南大学：是一所以理工为主，文、法、经、管、教育、艺术等学科协调发展的全国重点大学，是湖南省唯一一所2007年入选“985工程”的高等学府。2. 中南大学：是一所以冶金、采矿、材料科学与工程为主，涵盖工、理、管、文、法、教育等多个学科门类的全国重点大学，也是湖南省唯一一所入选“211工程”和“985工程”的高等学府。3. 国防科技大学：是一所以信息与电子工程为主，集理学、工学、管理学于一体的全国重点大学，是中国科学院、教育部和军方共同创办的一所现代化综合性大学。4. 湖南师范大学：是一所以师范类学科为主，涵盖理、工、文、法、史、哲、教育等多个学科门类的全国重点大学，也是湖南省唯一一所入选“211工程”的高等学府。5. 湖南农业大学：是一所以农业学科为主，涵盖理、工、农、管、法、教育等多个学科门类的全国重点大学，也是湖南省唯一一所入选“985工程”的高等学府。以上就是长沙的5所985大学。",
    "长沙有两所985大学，分别是中南大学和湖南大学。 1. 中南大学： 中南大学是中国教育部直属的全日制普通本专科高校，创建于1952年。该校位于湖南省长沙市，是湖南省省部共建高校，也是中部地区重点支持的高水平大学。中南大学在材料科学、工程、地球科学、交通运输、环境科学等领域具有较强的学科实力和国际影响力。 2. 湖南大学： 湖南大学，简称“湘大”，是湖南省人民政府与中国教育部共建高校，创建于1914年。该校坐落于湖南省长沙市岳麓山脚下，是湖南省重点支持的高水平大学。湖南大学以人文科学、社会科学、自然科学为主要发展方向，涵盖了文、理、工、医、农、法、经、教育、管理、艺术等多个学科门类。 这两所985大学在国内具有较高的学术声誉和师资力量，拥有优质的教育资源和科研条件。无论是师资力量、学科实力还是硬件设施，都能够为学生提供良好的学习环境和发展平台。另外，长沙作为湖南省的省会城市，交通便利、文化氛围浓厚，生活条件也相对较好。",
]

vote = Vote()
vote.stability(answers)
vote.majority_vote_weight(answers,[1,1,1,1,1,1])