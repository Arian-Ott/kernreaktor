from fastapi import FastAPI
import uvicorn
import asyncio
import aiomqtt
from config import settings
from db import Base, engine
from routes.oauth_routes import router as oauth_router
from routes.user_routes import user_router
from services.startup_service import startup_tasks
from services.mqtt_service import mqtt_listener
from routes.ecis_routes import ecis_router
from routes.daemon_routes import daemon_router

app = FastAPI(debug=settings.DEBUG, root_path="/api/v0")

# Routen registrieren
app.include_router(oauth_router)
app.include_router(user_router)
app.include_router(ecis_router)
app.include_router(daemon_router)


# Startup Routine
async def on_startup():
    if settings.DEBUG:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    startup_tasks()
    asyncio.create_task(mqtt_listener())


# Eventhandler einbinden
app.add_event_handler("startup", on_startup)


# Main Runner
def main():
    uvicorn.run(
        "main:app", host="0.0.0.0", port=settings.API_PORT, reload=settings.DEBUG
    )


if __name__ == "__main__":
    main()
