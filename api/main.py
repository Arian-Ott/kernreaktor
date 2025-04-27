from fastapi import FastAPI
import uvicorn
import asyncio
import asyncio_mqtt
from config import settings
from db import Base, engine
from routes.oauth_routes import router as oauth_router
from routes.user_routes import user_router
from services.startup_service import startup_tasks
from services.mqtt_service import mqtt_listener
app = FastAPI(debug=settings.DEBUG, root_path="/api/v0")

app.include_router(oauth_router)
app.include_router(user_router)




async def startup():
    if settings.DEBUG:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    startup_tasks()
    asyncio.create_task(mqtt_listener())

app.add_event_handler("startup", startup)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)
