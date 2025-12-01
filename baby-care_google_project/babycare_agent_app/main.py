import asyncio

from agent_interaction import interact_with_agent
from agent import *
from environment import configure_environment
from runner import *


def main():
    configure_environment()
    db_agent = create_agent_with_mcp()
    babycare_research_agent = create_babycare_research_agent()
    babycare_summarizer_agent = create_babycare_summarizer_agent()
    babycare_main_agent = create_main_agent(babycare_research_agent, babycare_summarizer_agent, db_agent)
    loop = asyncio.get_event_loop()
    # runner, user_id, session_id = loop.run_until_complete(setup_runner(db_agent))
    # runner, user_id, session_id = loop.run_until_complete(setup_session_compact_runner(babycare_main_agent))
    runner, user_id, session_id = loop.run_until_complete(setup_session_compact_auto_save_memory_runner(babycare_main_agent))
    loop.run_until_complete(interact_with_agent(runner, user_id, session_id))

if __name__ == "__main__":
    main()