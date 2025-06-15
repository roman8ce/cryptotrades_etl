from aiokafka import AIOKafkaConsumer
import asyncio
import asyncpg
import json
import config
from datetime import datetime

async def postgres_sender(message, conn):
    try:
        await conn.execute("""
            INSERT INTO raw_trades (symbol, price, quantity, trade_time)
            VALUES ($1, $2, $3, $4)
        """, message['s'], message['p'], message['q'], datetime.utcfromtimestamp(int(message['T'])/1000))
    except Exception as e:
        print(f'Postgres sender error: {e}')

async def kafka_receiver(consumer, conn):
    async for msg in consumer:
        await postgres_sender(msg.value, conn)

async def main():
    while True:
        try:
            conn = await asyncpg.connect(config.POSTGRE_URL)
            consumer = AIOKafkaConsumer(
                config.KAFKA_TOPIC,
                bootstrap_servers=config.KAFKA_URL,
                value_deserializer=lambda x: json.loads(x),
                auto_offset_reset='earliest',
                group_id='trades-consumer-group')

            await consumer.start()
            print('Consumer started')
            await kafka_receiver(consumer, conn)
        except Exception as e:
            print(f'Error in consumer: {e}')
            await asyncio.sleep(config.TIMEOUT)
        finally:
            await consumer.stop()
            await conn.close()
            print('Consumer stopped')
    
if __name__ == '__main__':
    asyncio.run(main())
