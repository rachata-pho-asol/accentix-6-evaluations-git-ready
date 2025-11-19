import os
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Result(BaseModel):
    result: bool
    comments: str

class Evaluator:
    def __init__(self, model_name: str = "gpt-5"):
        self.model_name = model_name
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        with open("evaluator_instructions.md", "r", encoding="utf-8") as file:
            self.instructions = file.read()

    def evaluate(self, turn):
        # Format the turn into a readable string user prompt
        user_prompt = "Evaluate the following turn:\n"
        user_prompt += f"Turn {turn["Turn"]}:\n"
        user_prompt += f"Question: {turn["Question"]}\n"
        user_prompt += f"Expected Chunk IDs: {turn["Expected Chunk ID"]}\n"
        user_prompt += f"Actual Chunk IDs: {turn["Actual Chunk ID"]}\n"
        user_prompt += f"Expected Answer: {turn["Expected Answer"]}\n"
        user_prompt += f"Actual Answer: {turn["Actual Answer"]}\n\n"

        response = self.client.responses.parse(
            model=self.model_name,
            instructions=self.instructions,
            input=user_prompt,
            text_format=Result
        )

        return response.output_parsed






