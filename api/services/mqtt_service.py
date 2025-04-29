from config import settings
import asyncio
import base64
import logging
from base64 import urlsafe_b64encode, urlsafe_b64decode
import aiomqtt
from services.ecis_service import ecies_decrypt, ecies_encrypt
import json
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
            
            #await client.publish("kernreaktor/status", b"kernreaktor-on")
            enc = ecies_encrypt(b"Test")
            enc = json.dumps(enc).encode()
       
            
            enc = urlsafe_b64encode(enc)
        
            await client.publish("kernreaktor/worker/", enc)
            async for message in client.messages:
                
                decrypted_message = decrypt_mqtt_request(message.payload)
                print(decrypted_message)
    except Exception as e:
        logging.error(f"[MQTT-Listener Fehler] {e}")  
        
        
def decrypt_mqtt_request(request: str) -> bytes:
    """
    Decrypts the incoming MQTT request (Base64-encoded JSON).
    Base64-decodes and prepares data for decryption.
    """
    try:

        decoded_request = base64.urlsafe_b64decode(request)

        # 2. JSON decode
        data = json.loads(decoded_request.decode())

        prepared_data = {
            "ephemeral_public_key": base64.urlsafe_b64decode(data["ephemeral_public_key"]),
            "iv": base64.urlsafe_b64decode(data["iv"]),
            "ciphertext": base64.urlsafe_b64decode(data["ciphertext"]),
            "tag": base64.urlsafe_b64decode(data["tag"]),
        }

       

   
        return ecies_decrypt(prepared_data)

    except Exception as e:
       
        logging.error(f"[MQTT-Decrypt Fehler] {e}")
    
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
            keepalive=60
        ) as client:
            await client.publish(topic, payload)
    except Exception as e:
        logging.error(f"[MQTT-Publish Fehler] {e}")