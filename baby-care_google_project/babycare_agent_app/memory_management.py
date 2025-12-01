from google.adk.agents.callback_context import CallbackContext

async def auto_save_to_memory(callback_context: CallbackContext):
    """Automatically save session to memory after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )