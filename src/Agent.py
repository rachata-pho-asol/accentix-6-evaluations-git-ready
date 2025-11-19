# from google import genai
# from helper import query_chroma
# types = genai.types

# tools = types.Tool(function_declarations=[query_chroma])
# config = types.GenerateContentConfig(
#     tools=[tools],
#     system_instruction=get_system_instruction()
# )

import requests

URL = "https://flowbuilderchat-genai.chatbotix.ai/api/generate_content"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "YOUR-AUTH_TOKEN"  # Replace with your actual token
}

class Agent:
    def __init__(self):
        # self.client = genai.Client()
        # self.contents = []
        self.system_instruction = get_system_instruction()
        self.history = []

    def generate_response(self, query: str | None):
        # self.save_query(query) if query else None
        # response = self.client.models.generate_content(
        #     model="gemini-2.5-flash",
        #     config=config,
        #     contents=self.contents,
        # )
        # self.save_response(response)
        # return response
        payload = {
            "template": "rag_sso",
            "model": "gemini-2.5-flash-lite",
            "system_instruction": self.system_instruction,
            "message": query,
            "genai_id": "SSO",
            "history": self.history
        }
        response = requests.post(URL, headers=HEADERS, json=payload)
        data = response.json()
        self.history = data["history"]
        return data

    # def save_query(self, query: str):
    #     self.contents.append(types.Content(role="user", parts=[types.Part(text=query)]))
    #
    # def save_response(self, response):
    #     self.contents.append(response.candidates[0].content)
    #
    # def save_function_call_response(self, result):
    #     self.contents.append(types.Content(role="user", parts=[types.Part.from_function_response(
    #         name="query_chroma",
    #         response= {"result": result}
    #     )]))