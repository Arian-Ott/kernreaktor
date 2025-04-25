from fastapi import FastAPI
import uvicorn
from config import settings
import os
from db import Base, engine
from routes.oauth_routes import router as oauth_router
from routes.user_routes import user_router
from services.startup_service import startup_tasks

app = FastAPI(debug=settings.DEBUG, root_path="/api/v0")

app.include_router(oauth_router)
app.include_router(user_router)


def startup():
    """
    Startup event handler for FastAPI.
    This function is called when the application starts.
    """
    if settings.DEBUG:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    startup_tasks()


app.add_event_handler("startup", startup)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)
