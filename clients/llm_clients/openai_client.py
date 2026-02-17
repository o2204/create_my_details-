from openai import OpenAI
from fastapi import UploadFile
import tempfile
import os 


class OpenAIClient:
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

        if not self.client:
            raise ValueError("OpenAI client is not found")
        
    def ask_with_file(
            self,
            query: str, 
            file: UploadFile,
            model: str = "gpt-4o-mini"
    ):
        suffix = os.path.splitext(file.filename)[-1]
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name
        
        try:
            uploaded_file = self.client.files.create(
                file=open(tmp_path, "rb"),
                purpose="assistants"
            )

            assistant = self.client.beta.assistants.create(
                name="File QA Assistant",
                model=model,
                tools=[{"type": "file_search"}],
                tool_resources={
                    "file_search": {
                        "vector_store_ids": []
                    }
                }
            )

            thread = self.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": query,
                        "attachments": [
                            {
                                "file_id": uploaded_file.id,
                                "tools": [{"type": "file_search"}]
                            }
                        ]
                    }
                ]
            )

            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id
            )

            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id,
            )

            return messages.data[0].content[0].text.value
        
        finally:
            os.remove(tmp_path)