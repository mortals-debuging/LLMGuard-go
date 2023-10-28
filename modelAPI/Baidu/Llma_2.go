package Baidu

const Llma2url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan_chinese_llama_2_7b?access_token="

type Llma2 struct {
	Baidu
	url string `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan_chinese_llama_2_7b?access_token=`
}

func NewLlma2() *Llma2 {
	baidu := NewBaidu()
	accessToken, _ := baidu.getAccessToken()
	baidu.url = Llma2url + accessToken
	llma2 := &Llma2{
		Baidu: *baidu,
	}
	return llma2
}
