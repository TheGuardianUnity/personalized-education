from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_PREFIX, DEBUG, PROJECT_NAME
from app.database.setup import engine  # Re-added engine import
from app.endpoints import hello, mistral_chat

# Note: Tables are not automatically created - will be managed separately

app = FastAPI(
    title=PROJECT_NAME,
    debug=DEBUG,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hello.router, prefix=API_PREFIX)
app.include_router(mistral_chat.router, prefix=API_PREFIX + "/mistral")

# Root endpoint
@app.get("/")
async def root():
    return {"status": "ok", "message": f"Welcome to {PROJECT_NAME}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)