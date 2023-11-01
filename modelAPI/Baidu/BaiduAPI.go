package Baidu

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"llmguard/modelAPI/Baidu/Token"
	"net/http"
	"strings"
)

type Baidu struct {
	ApiKey        string
	SecretKey     string
	AppId         string
	temperature   float64
	accessToken   string
	url           string
	maxLenMessage int
	messageQueue  []map[string]string
	headers       http.Header
}

func NewBaidu() *Baidu {
	token := Token.GetTokens().GetKeys()
	return &Baidu{
		ApiKey:        token.ApiKey,
		SecretKey:     token.SecretKey,
		AppId:         token.AppId,
		accessToken:   "",
		url:           "",
		headers:       http.Header{"Content-Type": {"application/json"}},
		maxLenMessage: 50,
		messageQueue:  make([]map[string]string, 0, 50),
	}
}

func (b *Baidu) AddMessage(mesg string, role string) string {
	if len(b.messageQueue) >= b.maxLenMessage {
		b.messageQueue = b.messageQueue[1:]
	}
	m := map[string]string{"role": role, "content": mesg}
	b.messageQueue = append(b.messageQueue, m)
	message := map[string]interface{}{
		"messages": b.messageQueue,
	}
	jsonMessage, err := json.Marshal(message)
	if err != nil {
		fmt.Println("Error:", err)
	}
	return string(jsonMessage)
}

func (b *Baidu) Invoke(mesg string, role string) (json.RawMessage, error) {
	message := b.AddMessage(mesg, role)
	if len(b.messageQueue) == 0 {
		return nil, errors.New("No message")
	}
	if b.url == "" {
		return nil, errors.New("no url specified")
	}
	req, err := http.NewRequest("POST", b.url, strings.NewReader(message))
	if err != nil {
		return nil, err
	}
	req.Header = b.headers
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	bodyBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil || resp.StatusCode != 200 {
		return nil, err
	}
	return bodyBytes, nil
}

func (b *Baidu) Response(mesg string, role string) (string, error) {
	jsonStr, err := b.Invoke(mesg, role)
	if err != nil {
		return "", err
	}
	var resp map[string]interface{}
	err = json.Unmarshal([]byte(jsonStr), &resp)
	if err != nil {
		return "", errors.New("result not found or is not a string")
	}

	result := resp["result"].(string)
	return string(result), nil
}

/**
 * 使用 AK，SK 生成鉴权签名（Access Token）
 * @return string 鉴权签名信息（Access Token）
 */
func (b *Baidu) getAccessToken() (string, error) {
	url := "https://aip.baidubce.com/oauth/2.0/token"
	postData := fmt.Sprintf("grant_type=client_credentials&client_id=%s&client_secret=%s", b.ApiKey, b.SecretKey)
	resp, err := http.Post(url, "application/x-www-form-urlencoded", strings.NewReader(postData))
	if err != nil {
		fmt.Println(err)
		return "", err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		return "", err
	}
	accessTokenObj := map[string]string{}
	json.Unmarshal([]byte(body), &accessTokenObj)
	return accessTokenObj["access_token"], nil
}
