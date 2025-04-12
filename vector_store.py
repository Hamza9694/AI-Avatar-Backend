import openai
from dotenv import load_dotenv
import json
import os
from assistent import create_assistent, save_id_to_file

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant = create_assistent()

vector_store = openai.beta.vector_stores.create(name="Ebizone AI Documents")
# file_paths = ["./docs/"]
docs_folder = "./docs/"
file_paths = [os.path.join(docs_folder, file) for file in os.listdir(docs_folder) if os.path.isfile(os.path.join(docs_folder, file))]

file_streams = [open(path, "rb") for path in file_paths]

file_batch = openai.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)


print("File batch status:", file_batch.status)
save_id_to_file("Vector Store ID: ", vector_store.id)

assistant = openai.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)
save_id_to_file("Assistent ID: ", assistant.id)


print("Assistant is ready and linked to the vector store.")

