from fastapi import FastAPI
from app.routes.ask_routes import router as ask_router
from app.routes.repo_routes import router as repo_router

app = FastAPI()
app.include_router(ask_router)
app.include_router(repo_router)

@app.get("/")
def get_home():
    return {
        "message":"Engbrain is working"
    }

@app.get("/status")
def get_status():
    return {
        "status":"ok"
    }
    

