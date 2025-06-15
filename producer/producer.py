from aiokafka import AIOKafkaProducer
import asyncio
import config
import websockets

async def kafka_sender(message, producer):
    await producer.send(config.KAFKA_TOPIC, message)

async def websocket_receiver(websocket, producer):
    while True:
        message = await websocket.recv()
        await kafka_sender(message, producer)

async def main():
    while True:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=config.KAFKA_URL, value_serializer=lambda x: x.encode(), compression_type="gzip")
            await producer.start()
            print('Producer started')
            websocket_clients = [await websockets.connect(url) for url in config.WEBSOCKET_URLS]
            tasks = [asyncio.create_task(websocket_receiver(websocket_client, producer)) for websocket_client in websocket_clients]
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            print(f'Error in producer: {e}')
            await asyncio.sleep(config.TIMEOUT)
        finally:
            await producer.stop()
            for websocket in websocket_clients:
                await websocket.close()
            print('Producer stopped')

if __name__ == '__main__':
    asyncio.run(main())
