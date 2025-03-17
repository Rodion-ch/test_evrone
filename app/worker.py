import asyncio

from services.common import close_connections
from services.kafka_consumer import run_kafka_consumer
from wait_for_services import wait_for_kafka, wait_for_postgres

if __name__ == "__main__":
    asyncio.run(wait_for_postgres())
    asyncio.run(wait_for_kafka())
    asyncio.run(run_kafka_consumer())
    asyncio.run(close_connections())
