

# Why LLMs Don't Have Memory by Default

Large Language Models (LLMs) like GPT are incredibly powerful at generating human-like text.  
However, **they do not have memory by default**, which means:

- They **do not remember previous interactions** across different sessions.
- They **cannot persist knowledge** about users, past conversations, or ongoing tasks beyond the current input context.


## 🧠 What "No Memory" Really Means

Unlike humans or stateful systems, LLMs are:

- **Stateless**: Every prompt is treated as a brand new request, with no awareness of previous conversations.
- **Context-limited**: They only "see" what’s in the current prompt (usually limited to a few thousand tokens).

---

## 📦 How LLMs Process Input

![Schema of Stateless LLM Input and Output](../images/default_behavior.png)

This is how LLMs work without memory:

1. The user sends a prompt.
2. The LLM generates a response based only on the text provided.
3. Once the response is returned, the model **forgets everything** — it does not retain any data from the interaction.

Unless memory is engineered on top, this cycle repeats every time.

---

## ⚠️ Why This Matters

Without memory:
- The user must constantly repeat context.
- The LLM can’t build a personalized relationship or learn user preferences.
- Multi-step tasks become harder to complete.
- Emotional, historical, or task continuity is lost between interactions.

---

## 🛠️ Workarounds (Engineered by Developers)

To overcome this limitation, developers design memory architectures **around** the LLM. These are some of the strategies used:

- **Storing chat history in databases** (SQL, VectorDBs, GraphDBs, etc.)
- **Using vector stores** for semantic memory retrieval (e.g., remembering topics or sentiments)
- **Graph databases** to model structured relationships, user profiles, interests, and more
- **Summarizing long interactions** to fit more context into the limited prompt size
- **Building agentic loops** that use tools and store relevant knowledge over time to guide behavior

---

> ⚡ **Bottom line:**  
> LLMs are powerful but forgetful.  
> Memory must be engineered externally to unlock their full potential.
