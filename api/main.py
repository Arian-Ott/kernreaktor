from fastapi import FastAPI
import uvicorn
from api.config import settings
import os
from api.db import Base, engine

app = FastAPI(debug=settings.DEBUG)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)
