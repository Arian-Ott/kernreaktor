import asyncio
import base64
import json
import logging

import aiomqtt

from api.config import settings
from api.services.crypto_service import decrypt, server_encrypt
# from api.services import message_handler  # Uncomment if needed


async def mqtt_listener():
    """
    Listens to MQTT topics and handles encrypted messages.
    """
    try:
        async with aiomqtt.Client(
            hostname=settings.MQTT_BROKER,
            port=settings.MQTT_PORT,
            # username=settings.MQTT_API_USER,
            # password=settings.MQTT_API_PASSWORD,
            keepalive=60,
        ) as client:
            await client.subscribe("kernreaktor/worker/#")
            await client.subscribe("kernreaktor/status/#")

            # Example encrypted message publish
            enc = json.dumps(server_encrypt("Test")).encode()
            enc_b64 = base64.urlsafe_b64encode(enc)
            await client.publish("kernreaktor/worker/", enc_b64)

            async for message in client.messages:
                decrypted = decrypt_mqtt_request(message.payload)
                if decrypted:
                    # Optionally handle message
                    # await message_handler.handle(decrypted)
                    print(f"Decrypted message: {decrypted.decode()}")

    except Exception as e:
        logging.error(f"[MQTT-Listener Fehler] {e}")


def decrypt_mqtt_request(request: bytes) -> bytes | None:
    """
    Decrypts the incoming MQTT request (Base64-encoded JSON).
    """
    try:
        decoded_json = base64.urlsafe_b64decode(request).decode()
        decrypted = decrypt(decoded_json.encode())
        return decrypted
    except Exception as e:
        logging.error(f"[MQTT-Decrypt Fehler] {e}")
        return None


async def mqtt_publish(topic: str, payload: dict):
    """
    Publishes a message to the specified MQTT topic.
    """
    try:
        async with aiomqtt.Client(
            hostname=settings.MQTT_BROKER,
            port=settings.MQTT_PORT,
            # username=settings.MQTT_API_USER,
            # password=settings.MQTT_API_PASSWORD,
            keepalive=60,
        ) as client:
            payload_json = json.dumps(payload).encode()
            encrypted = json.dumps(server_encrypt(payload_json)).encode()
            encoded = base64.urlsafe_b64encode(encrypted)
            await client.publish(topic, encoded)
    except Exception as e:
        logging.error(f"[MQTT-Publish Fehler] {e}")
