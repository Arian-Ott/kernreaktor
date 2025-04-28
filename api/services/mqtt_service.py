from config import settings
import asyncio
import aiomqtt

async def mqtt_listener():
    try:
        async with aiomqtt.Client(
            hostname=settings.MQTT_BROKER,
            port=settings.MQTT_PORT,
            # username=settings.MQTT_API_USER,
            # password=settings.MQTT_API_PASSWORD,
            keepalive=60
        ) as client:
            await client.subscribe("#")

            await client.publish("status", b"kernreaktor-on")

            async for message in client.messages:  
                print(f"Empfangen: Thema={message.topic}, Nachricht={message.payload.decode()}")

    except Exception as e:
        print(f"[MQTT-Listener Fehler] {e}")