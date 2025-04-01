
# Basic Chatbot

This `Chatbot` class is designed to manage a full conversational experience with a user, integrating OpenAI's chat models with persistent user and chat history management. Here's a breakdown of what it does:

---

### Core Functionalities:

#### 1. **Initialization (`__init__` method)**
- **Configuration & Client Setup:** Loads model names, token limits, and database paths from a config file.
- **Session Management:** Generates a unique `session_id` for each conversation session.
- **Component Initialization:**
  - `SQLManager`: Handles interactions with a database.
  - `UserManager`: Retrieves or manages user-specific information.
  - `ChatHistoryManager`: Manages ongoing chat history and conversation summaries.
- **History Summary Retrieval:** Fetches the most recent summary of past interactions to provide context in future chats.

#### 2. **Conversational Handling (`chat` method)**
- **System Prompt Preparation:** Constructs a dynamic system prompt based on:
  - User information (e.g., preferences, profile),
  - Summary of previous conversations,
  - Recent chat history.
- **Model Invocation:** Sends the user message and the system prompt to the OpenAI chat model and gets a response.
- **Chat History Management:**
  - Adds the user message and assistant response to the chat history.
  - Updates the ongoing summary of the conversation for future context.
- **Error Handling:** Returns a readable error message if anything goes wrong during the API call.

---

**Basic Chatbot Schema**

![Schema](../images/basic_chatbot.png)