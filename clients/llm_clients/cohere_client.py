import cohere
import logging

logger = logging.getLogger(__name__)


class CohereClient:
    def __init__(self, api_key: str, model: str):
        self.client = cohere.Client(api_key)
        self.model = model

    def ask(self, prompt: str) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                message=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Cohere API error: {e}")