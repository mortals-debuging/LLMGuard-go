# LLMguard

这是一个简单的调用文心一言，Chatgpt4的go代码项目

## Getting Started

你只需要在Tocken目录下创建包含自己tocken的.json文件即可。
例如
```json
#Baidu.json
{
    "API_KEY": "aaa",
    "SECRET_KEY": "aaa",
}
Openai.json
{
    "API_KEY": "sk-aaa"
}
```

使用时，可以调用以下函数创建。

```go
Baidu.NewErnieBot(),
Baidu.NewErnieBot4(),
Baidu.NewChatGLM(),
Baidu.NewLlma2(),
OpenAI.NewOpenAI(),
```
main.go文件是一个简单的示例，并将端口暴露在7860端口，你可以使用localhost:7860/ask?question=yourquestion 进行调用。

