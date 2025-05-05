from fastapi import APIRouter

mqtt_router = APIRouter(prefix="/mqtt", tags=["MQTT"], deprecated=True)


@mqtt_router.get("/connect")
async def connect():
    """
    Connect to the MQTT broker.
    """
    return {"message": "Connected to MQTT broker"}
