package main

import (
	"context"
	"encoding/json"
	"llmguard/modelAPI/Baidu"
	"llmguard/modelAPI/OpenAI"
	"log"
	"net/http"
	"sync"
	"time"
)

type Model interface {
	Response(mesg string, role string) (string, error)
}

func main() {
	http.HandleFunc("/ask", QuestionListen)
	log.Fatal(http.ListenAndServe(":7860", nil))
}

func handleRequest(question string, models []Model) []string {
	log.Println("--------------------handleRequest start---------------------")
	timeout := 30 * time.Second

	var wg sync.WaitGroup
	results := make([]string, len(models))
	for i, model := range models {
		wg.Add(1)
		go func(i int, model Model) {
			defer wg.Done()
			ctx, cancel := context.WithTimeout(context.Background(), timeout)
			defer cancel()

			done := make(chan bool, 1)
			go func() {
				results[i], _ = model.Response(question, "user")
				done <- true
			}()
			select {
			case <-ctx.Done():
				log.Println("第", i, "顺序超时")
			case <-done:
				log.Println("第", i, "顺序完成")
			}
		}(i, model)
	}
	wg.Wait()
	for _, result := range results {
		log.Println(result)
	}
	log.Println("--------------------handleRequest Finished---------------------")
	return results
}
func QuestionListen(w http.ResponseWriter, r *http.Request) {
	question := r.URL.Query().Get("question")
	if question == "" {
		http.Error(w, "请提供问题", http.StatusBadRequest)
		return
	}
	models := []Model{
		Baidu.NewErnieBot(),
		//Baidu.NewErnieBot4(),
		Baidu.NewChatGLM(),
		Baidu.NewLlma2(),
		OpenAI.NewOpenAI(),
	}
	results := handleRequest(question, models)
	resp := map[string][]string{
		"answers": results,
	}
	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(resp)
	if err != nil {
		return
	}
}
