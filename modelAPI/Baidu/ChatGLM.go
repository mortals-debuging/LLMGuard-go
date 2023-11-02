package Baidu

const CHATGLM = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token="

type ChatGLM struct {
	Baidu
	url string `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=`
}

func NewChatGLM() *ChatGLM {
	baidu := NewBaidu()
	accessToken, _ := baidu.getAccessToken()
	baidu.url = CHATGLM + accessToken
	chatGLM := &ChatGLM{
		Baidu: *baidu,
	}
	return chatGLM
}
