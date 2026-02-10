import cohere


class CohereClient:
    def __init__(self, api_key: str):
        self.client = cohere.Client(api_key)

    def ask(self, prompt: str, model: str) -> str:
        try:
            response = self.client.chat(
                model=model,
                message=prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"Cohere API error: {e}")