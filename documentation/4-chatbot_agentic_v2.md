# Agentic_Chatbot_v2

This second `Chatbot` class is an **advanced agentic version** of the first one. It not only handles chat but also **enables tool use** through **OpenAI function calling**, allowing the chatbot to take actions like updating user info or searching chat history dynamically. Let’s break down its functionalities and then highlight the key differences from the first version.

---

## 🔍 What This Class Does

### 1. **Initialization (`__init__`)**
- Similar base setup as before (OpenAI client, config, chat model, summary model, etc.).
- **Adds extra components:**
  - `Utils`: Utility methods, including one to convert Python functions to OpenAI-compatible JSON schemas.
  - `SearchManager`: Enables the chatbot to retrieve information from the SQL database using keyword/phrase-based search **(not semantic)**.
  - `agent_functions`: A list of available functions (with schema) the chatbot can call, such as:
    - `add_user_info_to_database`
    - `search_chat_history`

---

### 2. **Function Execution (`execute_function_call`)**
- Executes the appropriate function based on the name and arguments received from the OpenAI function call system.
- Returns a tuple of `state` (e.g. success/failure) and the `result`.

---

### 3. **Conversational Flow (`chat` method)**
This is where most of the new functionality lives:
- **Agentic loop:** Runs until the conversation state is "finished". This loop allows multiple function calls to occur before finalizing a response.
- **Dynamic system prompt:** Uses a specialized system prompt constructor `prepare_system_prompt_for_agentic_chatbot_v1` that includes:
  - User info
  - Chat history
  - Summary
  - Previous function calls and their results
- **Handles function calling:** If the LLM requests a function call:
  - Extracts function name and arguments
  - Executes the function via `execute_function_call`
  - Updates the prompt for the next loop iteration with the result of the call
- **Limits function calls:** If the number of function calls exceeds a threshold, the chatbot is instructed to proceed without further tools.
- **Returns final response** only once the model returns a message with plain content (not a function call).

---

## 🔄 Key Differences from the First Version

| Feature | **First Chatbot** | **Agentic Chatbot (This One)** |
|--------|------------------|------------------------------|
| **Chat Flow** | One-step, request-response | Multi-step with tool use and looping |
| **Function Calling** | ❌ Not supported | ✅ Supported (OpenAI function calling) |
| **Tools/Abilities** | Responds based on prompt only | Can take actions (e.g., update DB, search) |
| **Search Functionality** | ❌ Not available | ✅ Can search previous chats using keyword/phrase search on the SQL DB|
| **Utils Component** | ❌ Not used | ✅ Used to convert functions into schemas |
| **Prompt Strategy** | Simple system prompt | Enhanced prompt with function call context |
| **Error Feedback** | Basic exception handling | Detailed traceback included |
| **Agent Memory Management** | Only chat + summary | Chat + summary + function interaction history |

---

## 🧠 Summary
This updated version of the chatbot is designed to act more like an **intelligent agent**, capable of calling backend functions, incorporating their results, and iterating on its behavior. It adds **dynamic behavior**, **better memory handling**, and **tool use**.

---

**Agentic_Chatbot_v2 Schema**

![Schema 4](../images/chatbot_v2.png)