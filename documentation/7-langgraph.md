## 🧠 LangChain’s Second Strategy for Long-Term Memory

Now let’s look at the second memory approach — the one recently introduced by **LangChain’s CEO in their course with DeepLearning.AI**.

This design takes inspiration from **human memory systems**, breaking memory into three distinct types:

---

### 🧩 Types of Memory Modeled

1. **Semantic Memory**  
   - Stores *facts* about people, places, and things  
   - Example: “User prefers morning meetings” or “Pizza is John’s favorite food”  
   - Stored in a **VectorDB** for semantic retrieval  

2. **Episodic Memory**  
   - Captures *experiences* and *events*, like past interactions, preferences shared during chats, or actions taken  
   - This is the system's memory of "what happened"  

3. **Procedural Memory**  
   - Represents *instincts* — things the agent just *knows to do*  
   - These become part of the **system prompt**  
   - Example: How to respond politely, or follow a certain tone based on prior feedback  

---

### ⚙️ How It Works: The Memory Pipeline

LangChain’s design uses a **triage router** to decide where a memory belongs:
- Is it a fact? → Store it as *semantic*
- Is it an experience or event? → Store as *episodic*
- Is it a behavior change or instruction? → Store as *procedural*

When the user sends a message:
1. The agent processes it and routes relevant content into one of these memory types
2. The system retrieves past memory chunks as needed
3. It **reconstructs the prompt dynamically** with updated instructions, facts, and reminders
4. The LLM processes this enriched context and responds intelligently

---

### 🔧 Tools in Use

LangChain uses dedicated tools for each memory type:
- `manage_memory_tool` — updates or corrects memory entries
- `search_memory_tool` — retrieves relevant context
- `writing_tool`, `calendar_tool`, `scheduling_tool` — procedural actions triggered by memory

These tools work in concert, and the LLM decides whether to:
- Respond,
- Ignore,
- Or notify the user — depending on the context and the type of memory involved.


## Project schema

![Schema](../images/langgraph_course.png)
---

### 👨‍🏫 Let's See It in Action

Now I’ll show you how this architecture works in practice — we’ll go through the actual implementation and demonstrate how the system stores, routes, and retrieves different types of memory in real-time using LangChain’s latest agent stack.

Let’s dive into the code.
