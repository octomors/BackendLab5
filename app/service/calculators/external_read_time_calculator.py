import httpx

class ExternalReadTimeCalculator:

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    async def calculate(self, content: str) -> int:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/calculate",
                json={"text": content},
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()["read_time_minutes"]
