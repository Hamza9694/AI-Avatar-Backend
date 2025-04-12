from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import openai
import time
import os
from fastapi.middleware.cors import CORSMiddleware
from handle import chat_with_assistant
from dotenv import load_dotenv
import json
from assistent import create_thread, get_conversation_history

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def Get_GPT_Response(user_question):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "you are helpful assitent"}, 
                {"role": "user", "content": f"{user_question}"}],
        max_tokens=4096,
        temperature=0.1
    )
    response = response.choices[0].message.content
    return response

@app.get("/create-thread/")
async def get_thread_id():
    """
    Endpoint to create a new thread and return its ID.
    """
    try:
        thread_id = create_thread()
        return JSONResponse(content={"Thread_ID": thread_id.id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ASK-GPT/")
async def ask_gpt(message: str = Form(...), thread_id: str = Form(...)):
    """
    Endpoint to create a new thread and return its ID.
    """
    try:
        assistant_id = "asst_dj12ETYeP9fHsRdb7QSTeGdf"
        response = chat_with_assistant(assistant_id, thread_id, message)
        chat_history = get_conversation_history(thread_id)
        return JSONResponse(content={"Response": response, "Chat History": chat_history})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
