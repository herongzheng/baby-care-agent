import os
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import AgentTool, google_search
from google.adk.models.google_llm import Gemini

from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

from google.genai import types
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse

from google.adk.tools.load_memory_tool import load_memory
from memory_management import auto_save_to_memory

# from google.adk.models.lite_llm import LiteLlm

def create_agent_with_mcp(mcp_toolbox_endpoint=os.getenv("TOOLBOX_URL")):

    print("creating db agent...")

    retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )

    # may run with other LLM vendors using LiteLlm
    # model = LiteLlm(model="openai/gpt-5.1")

    db_admin_agent = LlmAgent(
        name="daily_event_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="""Autonomous and intelligent daily event agent, designed to interact directly with a MySQL database. "
            Capable of querying, modifying, or enriching baby daily pees data via the MCP server. 
            When you call MCP tools, you must always follow up with a final text response.
            Summarize the results in plain language. If no records are found, say "No records found.""",
        instruction=""" You are an autonomous daily event management agent with direct access to a MySql database via the MCP server.
            Your mission is to manage baby pee records (time, amount, whether it's normal, etc) effectively by invoking MCP tool set.
            The operations may involve insertion, retrieval, and deletion; 
            You workflow should follow the following guidance:
            - When you call MCP tools, the tool/function invocation itself is not sufficient, you must always follow up with a final text response that summarize the 
              what gets returned from the tool invocation. 
            - If no records are found, say "No records found.
            - Summarize the results in plain language. """,
        tools=[
            # 1. Instantiate the MCP Client (MCPToolset)
            MCPToolset(
                # 2. Configure the connection parameters (using HTTP in this case)
                connection_params=StreamableHTTPServerParams(
                    # Pass the full endpoint to the MCP Server
                    url=mcp_toolbox_endpoint,
                    # Optionally specify a toolset name if you grouped tools in your yaml
                    # toolset_name="my_mysql_toolset"

                ),
                # tool_filter=['get-records-by-volume', 'get-records-by-datetime-range',
                #              'get-records-by-volume-and-date-range',
                #              'insert-record-by-volume-and-datetime',
                #              'delete-record-by-id'],
            ),
            # Optional: Filter which specific tools to load from the server

        ],

        after_model_callback=after_model_callback_async,
        after_agent_callback=after_agent_callback_async,
        output_key="daily_event_info"
    )

    print("db agent created!")
    return db_admin_agent


async def after_agent_callback_async(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Asynchronous callback to ensure a final response exists using a temporary state flag.
    """
    print(f"▶ after_agent_callback for agent: {callback_context.agent_name}")

    # Check the temporary state to see if the main agent logic set the flag
    if not callback_context.state.get("temp:response_generated", False):
        print("[Callback] No response flagged in this turn. Providing a default.")

        # Return a Content object to inject this response as the final one
        return types.Content(
            parts=[types.Part.from_text(
                text="I couldn't generate a specific answer this time, but I am still ready for your next question."
            )],
            role="model",
        )

    print("[Callback] A response was flagged in this turn. Proceeding normally.")
    # Return None to use the agent's original response
    return None


# We need another callback that runs *during* the agent execution
# (specifically after the model generates content) to set this flag.
async def after_model_callback_async(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[
    LlmResponse]:
    final_response = False
    """Sets a temporary flag in the state if the model produced content."""
    if llm_response and llm_response.content and llm_response.content.parts:
        # Set a temporary state key (starts with temp:) which persists for the current turn
        callback_context.state["temp:response_generated"] = True
        for part in llm_response.content.parts:
            if part.text and part.text != "None":
                print(f"<<< DB Agent Response: {part.text}")
                final_response = True
            elif part.text == "None":
                print(f"<<< DB Agent Response (non-text): {part}")
            elif hasattr(part, "function_call"):
                print(f"<<< DB agent Function Call: {part.function_call}")

        if not final_response:
            callback_context.state["temp:response_generated"] = False

    return None  # Return None to allow the response to proceed


def create_babycare_research_agent():
    print("creating babycare research agent...")

    retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )

    babycare_research_agent = LlmAgent(
        name="babycare_research_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="""You are an agent specializing on baby caring. Given the user's question or query, you use only the
                google_search tool to form your best answer""",
        instruction=""" You are a specialized agent on the field of baby caring. Your only job is to use the google_search
                tool to find top 10 pieces of relevant information on the given question or query.""",
        tools=[google_search],
        output_key="babycare_research_findings"
    )
    print("babycare research agent created!")
    return babycare_research_agent


def create_babycare_summarizer_agent():
    print("creating babycare summarizer agent...")

    retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )

    babycare_summarizer_agent = LlmAgent(
        name="babycare_summarizer_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="""You are an agent specializing on summarizing baby caring related information. Given the 
                research findings: {babycare_research_findings}, you need to create a summary. """,
        instruction="""You are an agent specializing on baby caring. Given the research findings: {babycare_research_findings} 
                about babycare related query, present a concise summary as a bulleted list with 3-5 key points.""",
        output_key="babycare_summarizer_info"
    )
    print("babycare summarizer agent created!")
    return babycare_summarizer_agent


def create_main_agent(babycare_research_agent, babycare_summarizer_agent, db_agent):
    print("creating main agent...")
    retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )

    babycare_main_agent = LlmAgent(
        name="babycare_assistant",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a babycare assistant. Your goal is to answer the user's query by orchestrating a workflow.
        you may encounter two kinds of questions/queries. 
        - One is about the daily event about the baby. For example, "the baby peed at 3 am today, can you record it for later retrival?"
            "I want to know the pee records of the baby with pee volume being large". It may involve create&save, retrieve, delete records.
            For non-retrieval operations, `db agent` tool may return result indicating whether the operation is successful or not.
            For daily event or records about baby, you need to follow the two steps
            1. First, you MUST call the `db agent` tool to execute operations on the database that corresponds to user's intents.
            2. Then, always reserved the record id in the text response returned by `db agent` and present it in a professional way clearly to the user as your response.  
        - The other is the questions or information asked by the user about improving baby caring and how parents should do. 
            For example, "why my baby wakes up at early morning around 2 or 3 am?", "why parents get impatient easily 
            while raising a baby and how to improve the situation?"   
            For this kind of questions, you as a babycare assistant need to orchestrate the following workflow in three steps.
            1. First, you MUST call the `Babycare Research Agent` tool to find relevant information on the query provided by the user.
            2. Next, after receiving the research findings, you MUST call the `Babycare Summarizer Agent` tool to create a concise summary.
            3. Finally, present the final summary clearly to the user as your response.""",
        tools=[
            AgentTool(babycare_research_agent),
            AgentTool(babycare_summarizer_agent),
            AgentTool(db_agent),
            load_memory,
        ],
        after_agent_callback=auto_save_to_memory,

    )
    print("main agent created!")
    return babycare_main_agent
