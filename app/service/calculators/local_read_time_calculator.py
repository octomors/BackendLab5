class LocalReadTimeCalculator:
    WORDS_PER_MINUTE = 200

    async def calculate(self, content: str) -> int:
        words = len(content.split())
        minutes = words / self.WORDS_PER_MINUTE
        return max(1, int(minutes))
