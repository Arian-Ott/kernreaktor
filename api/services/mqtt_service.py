from api.config import settings
import asyncio
import base64
import logging
from base64 import urlsafe_b64encode, urlsafe_b64decode
import aiomqtt
from api.services.crypto_service import *
import json
from contextlib import contextmanager
import os

async def mqtt_listener():
    try:
        async with aiomqtt.Client(
            hostname=settings.MQTT_BROKER,
            port=settings.MQTT_PORT,
            # username=settings.MQTT_API_USER,
            # password=settings.MQTT_API_PASSWORD,
            keepalive=60
        ) as client:
            await client.subscribe("kernreaktor/worker/#")
            await client.subscribe("kernreaktor/status/#")
            

            async for message in client.messages:
                message.payload = message.payload.decode("utf-8")
                print(message.payload)
                decrypted_message = decrypt(message.payload)
                if decrypted_message:
                    await save_decrypted_message(message.topic, decrypted_message)  
    except Exception as e:
        logging.error(f"[MQTT-Listener Fehler] {e}")  
        
    
    
async def mqtt_publish(topic: str, payload: dict):
    """
    Publishes a message to the specified MQTT topic.
    """

    async with aiomqtt.Client(
        hostname=settings.MQTT_BROKER,
        port=settings.MQTT_PORT,
        # username=settings.MQTT_API_USER,
        # password=settings.MQTT_API_PASSWORD,
        keepalive=60
    ) as client:
        
        await client.publish(topic, payload)


async def save_decrypted_message(topic, message):
    """
    Save the decrypted message to a file.
    """
    if not os.path.exists("decrypted_messages"):
        os.makedirs("decrypted_messages")
    try:
        with open(f"decrypted_messages/{topic}.json", "w") as f:
            json.dump(message, f)
    except Exception as e:
        logging.error(f"[MQTT-Listener Fehler] {e}")