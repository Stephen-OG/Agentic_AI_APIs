from fastapi import APIRouter, HTTPException, Query
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel
from bson import ObjectId
from ..utils import conversation_serializer,character_serializer, user_serializer
from ..config.config import collection
from ..models.user import User
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

@router.get("/ai")
async def get_ai(user_id: str, message: str, character_id: str):
    userexist = await collection["users"].find_one({"_id": ObjectId(user_id)})
    if not userexist:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_serializer(userexist)

    character = await collection["characters"].find_one({"_id": ObjectId(character_id)})
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    conversation = await collection["conversations"].find_one({
        "user_id": user_id,
        "character_id": character_id
    })

    if not conversation:
        conversation = {
            "user_id": user_id,
            "character_id": character_id,
            "messages": [] 
        }
        await collection["conversations"].insert_one(conversation)

    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.4,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    prompt_template = PromptTemplate(
        input_variables=["history", "input"], 
        template=(
            """
            You are {name}, {personality}. 
            Your description: {description}. 
            Previous conversation: {history}
            Respond to the user in a way that reflects your personality.
            User: {input}
            """
        ),
        partial_variables={
            "name": character["name"],
            "personality": character["personality"],
            "description": character["description"]
        }
    )

    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=False,
        ai_prefix="AI",
        human_prefix="Me"
    )

    if conversation["messages"]:
        for msg in conversation["messages"]:
            if msg["user"]:
                memory.chat_memory.add_user_message(msg["user"])
            if msg["ai"]:
                memory.chat_memory.add_ai_message(msg["ai"])

    conversation_chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt_template,
    )

    response = conversation_chain.predict(input=message)

    conversation["messages"].append({"user": message, "ai": response})

    await collection["conversations"].update_one(
        {"user_id": user_id, "character_id": character_id},
        {"$set": {"messages": conversation["messages"]}}
    )

    return {"response": response}

@router.get("/conversation")
async def get_conversation(
    user_id: str,
    character_id: str,
    skip: int = Query(0, description="Number of messages to skip"),
    limit: int = Query(10, description="Number of messages to return")
):
    user = await collection["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    character = await collection["characters"].find_one({"_id": ObjectId(character_id)})
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    conversation = await collection["conversations"].find_one({
        "user_id": user_id,
        "character_id": character_id
    })

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = conversation["messages"][skip : skip + limit]

    return {
        "user_id": conversation["user_id"],
        "character_id": conversation["character_id"],
        "messages": messages
    }
