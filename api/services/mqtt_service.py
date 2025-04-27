from config import settings
import asyncio
import asyncio_mqtt

async def mqtt_listener():
    try:
        async with asyncio_mqtt.Client(
            hostname=settings.MQTT_BROKER,
            port=settings.MQTT_PORT,
            #username=settings.MQTT_API_USER,
            #password=settings.MQTT_API_PASSWORD,
            keepalive=60
        ) as client:
            async with client.filtered_messages("#") as messages:
                await client.subscribe("#")

                
                await client.publish("status", "kernreaktor-on")

                async for message in messages:
                    print(f"Empfangen: Thema={message.topic}, Nachricht={message.payload.decode()}")
    except Exception as e:
        print(f"[MQTT-Listener Fehler] {e}")