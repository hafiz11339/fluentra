from src.response import BuildJSONResponses


class ChatService:
    def __init__(self):
        pass
    async def llm_chat(self, message: str) -> str:
        # Implement your LLM chat logic here
        response = f"Echo: {message}"
        return BuildJSONResponses.success_response(
                    response, "LLM chat response"
                )