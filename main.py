from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from api.controllers.user import router as user_router
from pydantic import BaseModel

# Define a simple model for the user input
class InputData(BaseModel):
    user_input: str

# FastAPI App
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify ['http://localhost:3000']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "User Home"}

@app.post("/get_ai_response/")
async def get_ai_response(data: InputData):
    # Here you can integrate your Agentic AI logic
    # This is just an example response
    ai_response = f"AI Response to '{data.user_input}'"
    return {"response": ai_response}

app.include_router(user_router)