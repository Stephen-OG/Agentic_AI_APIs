# Helper Function to Convert MongoDB Document
def user_serializer(user) -> dict:
    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"],"username": user["username"]}
def conversation_serializer(conversation) -> dict:
    return {"id": str(conversation["_id"]), "user_id": conversation["user_id"], "character_id": conversation["character_id"]}
def character_serializer(character) -> dict:
    return {"id": str(character["_id"]), "name": character["name"], "personality": character["personality"],"description": character["description"]}

def create_character_prompt(character: dict, user_message: str) -> str:
        prompt_template = (
            "You are {name}, {personality}. "
            "Your description: {description}. "
            "Respond to the user in a way that reflects your personality. "
            "User: {user_message}"
        )
        return prompt_template.format(
            name=character["name"],
            personality=character["personality"],
            description=character["description"],
            user_message=user_message
        )