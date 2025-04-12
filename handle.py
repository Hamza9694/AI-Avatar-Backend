import openai
from dotenv import load_dotenv
import json
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_assistant(assistant_id, thread_id, user_query):
    try:
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_query
        )

        run = openai.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        messages = list(openai.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))
        if messages:
            return messages[0].content[0].text.value

        return "Sorry, I am facing some problem entertaining your query, could you please try again!"

    except Exception as e:
        return f"An error occurred: {str(e)}"
