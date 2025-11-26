from email.message import EmailMessage

import aiosmtplib


class SMTP:
    def __init__(self, host: str, port: int, admin_email: str):
        self.host = host
        self.port = port
        self.admin_email = admin_email

    async def send(self, recipient: str, subject: str, body: str):
        message = EmailMessage()
        message["From"] = self.admin_email
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(
            message,
            sender=self.admin_email,
            recipients=[recipient],
            hostname=self.host,
            port=self.port,
        )
