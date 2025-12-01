from google.genai import types

async def call_agent_async(query: str, runner, user_id, session_id):
    print(f"\n>>> User Query: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if not (event.is_final_response()) and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text and part.text != "None":
                    print(f"<<< Agent Response: {part.text}")

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break
    print(f"<<< Agent Response: {final_response_text}")
    return final_response_text

async def interact_with_agent(runner, user_id, session_id):
    print("Start chatting with the agent ... Type 'exit' to end the conversation.")
    while True:
        user_input = input("\n>>> Enter your message: ")
        if user_input.lower() == 'exit':
            print("Ending the conversation.")
            break
        await call_agent_async(user_input, runner, user_id, session_id)
