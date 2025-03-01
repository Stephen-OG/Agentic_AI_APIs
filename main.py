from fastapi import FastAPI, HTTPException
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from api.controllers.user import router as user_router
from api.controllers.agent import router as ai_agent

# FastAPI App
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allow all origins, or specify ['http://localhost:3000']
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "User Home"}

app.include_router(user_router)
app.include_router(ai_agent)