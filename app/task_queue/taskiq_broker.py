import os
import taskiq_fastapi
from taskiq_aio_pika import AioPikaBroker

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")

broker = AioPikaBroker(
    url=RABBITMQ_URL,
)

taskiq_fastapi.init(broker, "main:main_app")
