from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json
import time



async def execute(request):
    flight_agent = Agent(
        name="datasaver_agent",
        model="gemini-2.5-flash-lite", #"openai/gpt-4o", #LiteLlm("openrouter/meta-llama/llama-3-70b-instruct"),
        description="Download nifty50 data for given years.",
        instruction=(
            "Given nifty50startyear and nifty50endyear, Fetch data of Nifty50 starting nifty50startyear upto nifty50endyear and save file in current folder. "
            "Include type of file and location where you are saving. "
            "Respond in plain English. Keep it concise and well-formatted."
        )
    )
    USER_ID = "user_1"
    SESSION_ID = "session_001"
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="flight_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    time.sleep(5)  # Simulate some processing delay
    runner = Runner(
        agent=flight_agent,
        app_name="flight_app",
        session_service=session_service
    )
    prompt = (
        f"User wants to download data of nifty50 from year {request['nifty50startyear']} upto year {request['nifty50endyear']}, "
        f"Include type of file and location where you are saving.  "
        f"Respond in plain English. Keep it concise and well-formatted."
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    time.sleep(5)  # Simulate some processing delay
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"type_and_location": event.content.parts[0].text}
            # response_text = event.content.parts[0].text
            # try:
            #     parsed = json.loads(response_text)
            #     if "flight" in parsed and isinstance(parsed["flight"], list):
            #         return {"flight": parsed["flight]}
            #     else:
            #         print("'flight' key missing or not a list in response JSON")
            #         return {"flights": response_text}  # fallback to raw text
            # except json.JSONDecodeError as e:
            #     print("JSON parsing failed:", e)
            #     print("Response content:", response_text)
            #     return {"flights": response_text}  # fallback to raw text
