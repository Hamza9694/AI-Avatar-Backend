import openai
from dotenv import load_dotenv
import json
import os
from datetime import datetime, timedelta

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

threads = {}

def cleanup_old_threads():
    now = datetime.now()
    keys_to_delete = [thread_id for thread_id, timestamp in threads.items() if now - timestamp > timedelta(hours=24)]
    for key in keys_to_delete:
        del threads[key]
        openai.beta.threads.delete(key)

def save_id_to_file(id_type, id_value, filename="IDs.txt"):
    with open(filename, "a+") as file:  # "a+" allows both append and read
        file.write(f"{id_type}: {id_value}\n")
        file.seek(0)  # Move cursor to the beginning to read the file
        content = file.read()
    return content  # Return the file content if needed

def create_thread():
    thread = openai.beta.threads.create()
    #save_id_to_file("Thread ID: ", thread.id)
    threads[thread.id] = datetime.now()
    cleanup_old_threads()
    return thread

def create_assistent():
    assistant = openai.beta.assistants.create(
        name="AI Assistant",
        
        instructions = "You are a helpful assistent trained on some data. You will try to answer user queries as best as possible reffering to the data provided you in the files.",
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
    )
    return assistant

def get_conversation_history(thread_id):
    # Fetch thread messages
    thread_messages = openai.beta.threads.messages.list(thread_id)
    
    # Initialize an empty list to store chat history
    chat_history = []
    
    # Process each message
    for message in thread_messages.data:
        # Extract role and content
        role = message.role
        content = " ".join([block.text.value for block in message.content if block.type == "text"])
        
        # Append the formatted message to the chat history
        chat_history.append({
            "role": role,
            "content": content,
            "timestamp": message.created_at
        })
    
    return json.dumps(chat_history, indent=4)
