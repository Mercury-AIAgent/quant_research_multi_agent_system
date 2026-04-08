from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

host_agent = Agent(
    name="host_agent",
    model="gemini-2.5-flash-lite", #"openai/gpt-4o", #LiteLlm("openrouter/meta-llama/llama-3-70b-instruct"), # "openai/gpt-4o"
    description="Coordinates quant assignment by calling datasaver, news, and coder agents.",
    instruction="You are the host agent responsible for orchestrating quant tasks. "
                "You call external agents to gather data and save, related news, and generate code, then return a news bullet points and results on monthly basis."
)
session_service = InMemorySessionService()
runner = Runner(
    agent=host_agent,
    app_name="host_app",
    session_service=session_service
)
USER_ID = "user_host"
SESSION_ID = "session_host"

async def execute(request):
    # Ensure session exists
    session_service.create_session(
        app_name="host_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    prompt = (
        f"Fetch data of Nifty50 starting from {request['nifty50startyear']} upto {request['nifty50endyear']} via datasaver agent and save file in current folder."
        f"then call news agent to check monthly nifty50 behavior of all months between {request['nifty50startyear']} and {request['nifty50endyear']} via news agent."
        f"then call coder agent to generate code for comparing monthly performance of nifty50 in all years starting from {request['nifty50startyear']} upto {request['nifty50endyear']}"
        f"nifty50 data is saved in current folder. two parameters of function should be nifty50startyear and nifty50end year and return type should be dictionary where keys will be years and values will be list of monthly returns of nifty50. print the code as per coder agent instructions."
        f"Call the datasaver, news, and coder agents for results."
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"summary": event.content.parts[0].text}
