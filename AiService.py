import ollama


def chat(message):
    system_prompt = {
        "role": "system",
        "content": """
        너는 매우매우 상냥하고 따뜻한 타로 전문 상담가야.
        유저가 고민과 함께 뽑은 타로 카드를 알려 주면, 너는 상냥하게 유저가 선택한 카드에 대해 설명해 줘야 해.
        물론, 유저의 고민과 맥락에 맞게 설명해 줘야 해.
        유저가 궁금한 것이 있다면 그에 맞게 답변해 줘야 해.
        """
    }

    response = ollama.chat(
        model = 'llama3.1',
        messages = [
            system_prompt,
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return response['message']['content']

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_api(message: Message):
    response = chat(message.message)
    return {"response": response}