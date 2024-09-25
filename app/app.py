from fastapi import FastAPI
# from app.routes.routes import router as api_router  # Importa el router desde routes.py

app = FastAPI()

@app.get("/")
def is_running():
    return {"running": True}

# app.include_router(api_router)