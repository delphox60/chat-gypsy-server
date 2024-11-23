import ollama
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Define the message format using Pydantic
class Message(BaseModel):
    message: str

# Chat function with the Ollama model
def chat(message):
    system_prompt = {
        "role": "system",
        "content": """
        당신은 매우매우 상냥하고 따뜻한 타로 전문 상담가입니다.
        궁금한 점과 함께 뽑은 타로 카드를 알려 주면, 상냥하고 친절하게 선택한 카드에 대해 설명해 줘야 합니다.
        뽑은 카드에 대해 간략히 설명해 주세요. 
        맥락과 상황에 맞게 상담과 조언을 해 주세요.
        집시처럼 신비로운 분위기로 예언하듯이 말해 주세요.
        markdown으로 예쁘게 포매팅 해주세요.
        친절하게 존댓말로 답변해 주세요.
        """
    }

    response = ollama.chat(
        model='llama3.1',
        messages=[
            system_prompt,
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return response['message']['content']

# Define the chat API endpoint
@app.post("/chat")
def chat_api(message: Message):
    response = chat(message.message)
    print(response)
    return {"response": response}

# Explicitly handle OPTIONS requests
@app.options("/chat")
def options_chat():
    return Response(status_code=200)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
