# Helper Function to Convert MongoDB Document
def user_serializer(user) -> dict:
    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}