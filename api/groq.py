import os
from dotenv import load_dotenv
from pydantic import PrivateAttr
from langchain_core.language_models.base import BaseLanguageModel
from groq import Groq
from typing import List, Optional, Any
from langchain_core.outputs import LLMResult


load_dotenv()

# Set up Groq API key and URL
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqLanguageModel(BaseLanguageModel):
    model_name: str = "llama-3.3-70b-specdec"

    _client: Groq = PrivateAttr()

    def __init__(self, api_key: str, **kwargs):
        super().__init__(**kwargs)
        self._client = Groq(api_key=api_key)

    def create_character_prompt(self, character: dict, user_message: str) -> str:
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
    
    def generate_prompt(self, prompts: List[str], stop: Optional[List[str]] = None, **kwargs) -> LLMResult:
        responses = []
        for prompt in prompts:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            responses.append(response.choices[0].message["content"].strip())
        return LLMResult(generations=[[resp] for resp in responses])

    def agenerate_prompt(self, prompts: List[str], stop: Optional[List[str]] = None, **kwargs) -> LLMResult:
        """Asynchronous version of `generate_prompt`."""
        responses = []
        for prompt in prompts:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            print(responses.append(response.choices[0].message.content.strip())) 
        return LLMResult(generations=[[resp] for resp in responses])
    
    def predict(self, text: str, max_tokens: int = 150, temperature: float = 0.5) -> str:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": text}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message["content"].strip()

    async def apredict(self, text: str, max_tokens: int = 150, temperature: float = 0.5) -> str:
        response = await self._client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": text}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message["content"].strip()

    def predict_messages(self, messages: List[dict], **kwargs) -> str:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message["content"].strip()

    async def apredict_messages(self, messages: List[dict], **kwargs) -> str:
        """Handle multiple messages asynchronously."""
        response = await self._client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message["content"].strip()

    def invoke(self, input: str, **kwargs) -> Any:
        """General invocation method."""
        return self.predict(input, **kwargs)
    




# # def create_character_prompt(character: dict, user_message: str) -> str:
# #     prompt_template = (
# #         "You are {name}, {personality}. "
# #         "Your description: {description}. "
# #         "Respond to the user in a way that reflects your personality. "
# #         "User: {user_message}"
# #     )
# #     return prompt_template.format(
# #         name=character["name"],
# #         personality=character["personality"],
# #         description=character["description"],
# #         user_message=user_message
# #     )

# # llm = ChatGroq(model_name="llama-3.3-70b-specdec", groq_api_key=GROQ_API_KEY, temperature=0.7)
# # memory = ConversationBufferMemory()
# # conversation = ConversationChain(llm=llm, memory=memory)
# def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.5) -> str:
#         response = self.client.generate(
#             model=self.model_name,
#             prompt=prompt,
#             max_tokens=max_tokens,
#             temperature=temperature
#         )
#         return response.choices[0].text.strip()

#     async def agenerate(self,prompt: str, max_tokens: int = 150, temperature: float = 0.5) -> str:
#         # Asynchronous version (if needed)
#         response = await self.client.chat.completions.create(
#             model=self.model_name,
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=max_tokens,
#             temperature=temperature
#         )
#         return response.choices[0].message["content"].strip()