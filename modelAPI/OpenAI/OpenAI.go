package OpenAI

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"llmguard/modelAPI/OpenAI/Token"
	"net/http"
	"strings"
)

type OpenAI struct {
	ApiKey        string
	url           string
	model         string
	temperature   float64
	maxLenMessage int
	messageQueue  []map[string]string
	headers       http.Header
}

func NewOpenAI() *OpenAI {
	token := Token.GetTokens().GetKeys()
	return &OpenAI{
		ApiKey: token.ApiKey,
		url:    "https://api.openai.com/v1/chat/completions",
		headers: http.Header{"Content-Type": {"application/json"},
			"Authorization": {"Bearer " + token.ApiKey}},
		model:         "gpt-3.5-turbo",
		temperature:   0.7,
		maxLenMessage: 50,
		messageQueue:  make([]map[string]string, 0, 50),
	}
}
func (o *OpenAI) AddMessage(mesg string, role string) string {
	if len(o.messageQueue) >= o.maxLenMessage {
		o.messageQueue = o.messageQueue[1:]
	}
	m := map[string]string{"role": role, "content": mesg}
	o.messageQueue = append(o.messageQueue, m)
	message := map[string]interface{}{
		"model":       o.model,
		"messages":    o.messageQueue,
		"temperature": o.temperature,
	}
	jsonMessage, err := json.Marshal(message)
	if err != nil {
		fmt.Println("Error:", err)
	}
	return string(jsonMessage)
}
func (o *OpenAI) Invoke(mesg string, role string) (json.RawMessage, error) {
	message := o.AddMessage(mesg, role)
	if len(o.messageQueue) == 0 {
		return nil, errors.New("No message")
	}
	if o.url == "" {
		return nil, errors.New("no url specified")
	}
	req, err := http.NewRequest("POST", o.url, strings.NewReader(message))
	if err != nil {
		return nil, err
	}
	req.Header = o.headers
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	bodyBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil || resp.StatusCode != 200 {
		return nil, errors.New("Error: " + string(bodyBytes))
	}
	return bodyBytes, nil
}

func (o *OpenAI) Response(mesg string, role string) (string, error) {
	jsonStr, err := o.Invoke(mesg, role)
	if err != nil {
		return "", err
	}
	var resp map[string]interface{}
	err = json.Unmarshal([]byte(jsonStr), &resp)
	if err != nil {
		return "", errors.New("result not found or is not a string")
	}

	choices := resp["choices"].([]interface{})
	message := choices[0].(map[string]interface{})["message"].(map[string]interface{})
	content := message["content"].(string)

	return string(content), nil
}
