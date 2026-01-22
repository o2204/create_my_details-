from clients.llm_clients.cohere_client import CohereClient


class LLMRouter:
    def __init__(self, cohere_client: CohereClient):
        self.cohere_client = cohere_client

    def route(self, query: str) -> CohereClient:
        # future: route based on query
        return self.cohere_client
