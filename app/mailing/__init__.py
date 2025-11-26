from typing import Annotated, Protocol
from fastapi import Depends
from .smtp import SMTP


class Mail(Protocol):

    async def send(self, recipient: str, subject: str, body: str) -> None: ...


# Все данные должны браться из переменных окружения и конфигурации
def get_mail() -> Mail:
    return SMTP(
        host="localhost",
        port=1025,
        admin_email="admin@localhost",
    )


MailDep = Annotated[Mail, Depends(get_mail)]
