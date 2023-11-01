package Token

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"sync"
)

type Token struct {
	ApiKey    string `json:"API_KEY"`
	SecretKey string `json:"SECRET_KEY"`
	AppId     string `json:"APP_ID"`
}

type Tokens struct {
	configs []Token
	index   int
	sync.Mutex
}

var instance *Tokens
var once sync.Once

func init() {
	UpdateTokens()
}
func UpdateTokens() {
	once.Do(func() {

		instance = &Tokens{}
		instance.configs = []Token{}
		instance.index = 0

		files, err := os.ReadDir("./modelAPI/Baidu/Token")
		if err != nil {
			fmt.Println("Error reading directory:", err)
			os.Exit(1)
		}
		for _, file := range files {
			if file.IsDir() || !strings.HasSuffix(file.Name(), ".json") {
				continue
			}

			filePath := "./modelAPI/Baidu/Token/" + file.Name()
			f, err := os.Open(filePath)
			if err != nil {
				fmt.Println("Error opening file:", err)
				os.Exit(1)
			}

			var config Token
			err = json.NewDecoder(f).Decode(&config)
			if err != nil {
				fmt.Println("Error decoding JSON from file:", err)
				os.Exit(1)
			}
			f.Close() // Close the file immediately after reading
			instance.configs = append(instance.configs, config)
		}
	})
}
func GetTokens() *Tokens {
	return instance
}

func (t *Tokens) GetKeys() Token {
	t.Lock()
	defer t.Unlock()
	if len(t.configs) == 0 {
		panic("No token available")
	}
	token := t.configs[t.index]
	t.index = (t.index + 1) % len(t.configs)
	return token
}
