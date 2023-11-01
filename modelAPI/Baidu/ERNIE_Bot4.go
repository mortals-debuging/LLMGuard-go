package Baidu

const ErnieBot4url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="

type ErnieBot4 struct {
	Baidu
	url string `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=`
}

func NewErnieBot4() *ErnieBot4 {
	baidu := NewBaidu()
	accessToken, _ := baidu.getAccessToken()
	baidu.url = ErnieBot4url + accessToken
	ernieBot := &ErnieBot4{
		Baidu: *baidu,
	}
	return ernieBot
}
