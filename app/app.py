from fastapi import FastAPI
from app.routes.routes import router as api_router  # Importa el router desde routes.py

app = FastAPI()

app.include_router(api_router)