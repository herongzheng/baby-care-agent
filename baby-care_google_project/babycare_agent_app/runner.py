from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.apps.app import App, EventsCompactionConfig

async def setup_runner(db_agent):

    session_service = InMemorySessionService()
    APP_NAME = "agents"
    USER_ID = "user_001"
    SESSION_ID = "session_001"
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    runner = Runner(
        agent=db_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    return runner, USER_ID, session.id

async def setup_session_compact_runner(db_agent):

    session_service = InMemorySessionService()
    APP_NAME = "agents"
    USER_ID = "user_001"
    SESSION_ID = "session_001"
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    app_session_compact = App(
        name=APP_NAME,
        root_agent=db_agent,
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=3,  # Trigger compaction every 3 invocations
            overlap_size=1,  # Keep 1 previous turn for context
        ),
    )
    runner = Runner(
        app=app_session_compact,
        session_service=session_service
    )

    return runner, USER_ID, session.id

async def setup_session_compact_auto_save_memory_runner(db_agent):

    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    APP_NAME = "agents"
    USER_ID = "user_001"
    SESSION_ID = "session_001"
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    app_session_compact = App(
        name=APP_NAME,
        root_agent=db_agent,
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=3,  # Trigger compaction every 3 invocations
            overlap_size=1,  # Keep 1 previous turn for context
        ),
    )
    runner = Runner(
        app=app_session_compact,
        session_service=session_service,
        memory_service=memory_service
    )

    return runner, USER_ID, session.id