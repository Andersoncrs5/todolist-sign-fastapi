# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# uvicorn main:app --reload

import logging
from fastapi import FastAPI
from api.controllers import auth_controller, user_controller, task_controller
from api.configs.db.database import create_tables
from contextlib import asynccontextmanager
from typing import Final

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger: Final[logging.Logger] = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    
    create_tables()
    yield
    logger.info("Shutting down the application...")

app: Final[FastAPI] = FastAPI(
    lifespan=lifespan, 
    title="To do list with system auth with jwt", 
    version="1.0.0"
    )

app.include_router(task_controller.router)
app.include_router(auth_controller.router)
app.include_router(user_controller.router)