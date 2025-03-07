

def prepare_system_prompt(user_info, chat_summary, chat_history):
    user_info = ""
    chat_summary = ""
    chat_history = ""
    prompt = """You are a professional assistant of the following user.

    {user_info}

    Here is a summary of the previous conversation history:

    {chat_summary}

    Here is the previous conversation between you and the user:

    {chat_history}
    """

    return prompt.format(
        user_info=user_info,
        chat_summary=chat_summary,
        chat_history=chat_history,
    )


def prepare_system_prompt_for_agentic_chatbot_v1(user_info: str, chat_summary: str, chat_history: str, search_result_section: str) -> str:

    prompt = """## You are a professional assistant of the following user.

    {user_info}

    ## Here is a summary of the previous conversation history:

    {chat_summary}

    ## Here is the previous conversation between you and the user:

    {chat_history}

    ## You have access to two functions: search_chat_history and add_user_info_to_database.

    - If you need more information about the user or details from previous conversations to answer the user's question, use the search_chat_history function.
    - Monitor the conversation, and if the user provides any of the following details that differ from the initial information, call this function to update 
    the user's database record.

    ### Keys for Updating the User's Information:

    - name: str
    - last_name: str
    - age: int
    - gender: str
    - location: str
    - occupation: str
    - interests: list[str]
    
    Important: The add_user_info_to_database function expects a dictionary as input. Ensure you provide the correct key-value pairs when calling it.

    {search_result_section}
    """

    return prompt.format(
        user_info=user_info,
        chat_summary=chat_summary,
        chat_history=chat_history,
        search_result_section=search_result_section
    )
