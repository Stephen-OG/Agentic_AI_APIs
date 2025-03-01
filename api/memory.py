from .config.config import collection

class ConversationMemory:
    @staticmethod
    def save_message(session_id: str, user_input: str, bot_response: str):
        """Save a chat message to MongoDB"""
        collection["memory"].insert_one({
            "session_id": session_id,
            "user_input": user_input,
            "bot_response": bot_response
        })

    @staticmethod
    def get_chat_history(session_id: str):
        """Retrieve conversation history for a session"""
        history = collection["memory"].find({"session_id": session_id})
        return [{"user": msg["user_input"], "bot": msg["bot_response"]} for msg in history]
