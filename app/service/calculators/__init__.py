from typing import Annotated, Protocol
from fastapi import Depends
from .local_read_time_calculator import LocalReadTimeCalculator


class ReadTimeCalculator(Protocol):

    async def calculate(self, content: str) -> int: ...


def get_read_time_calculator() -> ReadTimeCalculator:
    return LocalReadTimeCalculator()

    # return ExternalReadTimeCalculator(
    #     api_url=settings.READ_TIME_API_URL,
    #     api_key=settings.READ_TIME_API_KEY
    # )


ReadTimeCalculatorDep = Annotated[ReadTimeCalculator, Depends(get_read_time_calculator)]
