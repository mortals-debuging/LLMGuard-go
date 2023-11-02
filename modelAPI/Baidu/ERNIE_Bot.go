package Baidu

const ErnieBoturl = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token="

type ErnieBot struct {
	Baidu
	url string `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=`
}

func NewErnieBot() *ErnieBot {
	baidu := NewBaidu()
	accessToken, _ := baidu.getAccessToken()
	baidu.url = ErnieBoturl + accessToken
	ernieBot := &ErnieBot{
		Baidu: *baidu,
	}
	return ernieBot
}
