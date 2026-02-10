from clients.llm_clients.cohere_client import CohereClient


class ChatService:
    def __init__(self, cohere_client: CohereClient):
        self.cohere_client = cohere_client

    def ask(self, query: str) -> str:
        try: 
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")
            return self.cohere_client.ask(query, model="command-r-plus") ## Can i use the constant here instead of hardcoding the model name?
        
        except Exception as e:
            raise Exception(f"Error in chat service: {e}")