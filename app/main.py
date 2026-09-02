from fastapi import FastAPI
from app.routes.ask_routes import router as ask_router
from app.routes.repo_routes import router as repo_router
from app.routes.runbook_routes import router as runbook_router
from app.routes.symbol_routes import router as symbol_router

app = FastAPI()
app.include_router(ask_router)
app.include_router(repo_router)
app.include_router(symbol_router)
app.include_router(runbook_router)

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
    

