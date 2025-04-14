# 🧩 Frameworks for Building Agentic Memory: Theory Before Code

Now that we've explored how memory systems work conceptually and seen how to design our own chatbot agents, it's time to talk about **frameworks**.

Frameworks allow an easier development, especially when it comes to handling:
- Memory storage
- Retrieval logic
- Agent loops
- Prompt construction

As this space matures, choosing the right foundation becomes critical for long-term stability and scalability.

---

## 🥇 LeTTA

LeTTA introduced many of the ideas that pushed the field of long-term agentic memory forward.  
They've published a framework that embodies their research and philosophy.

However, I personally **do not recommend using the LeTTA framework for production systems**, and here's why:

- ⚠️ It's relatively **new** and **immature** in terms of ecosystem and tooling
- 🧩 Larger, well-supported platforms like LangChain already offer **equivalent capabilities**
- 🧪 The **sample code** they provided in their public course **is already outdated and non-functional**
- 🔧 Debugging and extending the framework may require significant manual effort

You're free to explore and learn from it — but for production-level reliability, I'd recommend more mature options.

---

## 🔄 LangChain: The Production-Ready Option

While developing this project, I noticed that **LangChain introduced built-in support for long-term memory** in its agent framework — and it's both robust and well-documented.

LangChain currently supports **two distinct memory strategies**, and we'll explore both in this session.

---

## 🧠 Strategy 1: Hybrid Memory with Vector + Graph Databases

![LangChain Memory Architecture](../images/langgraph_1.png)

This architecture uses a **hybrid memory system**:

- 🟣 **VectorDB**: Stores embeddings of past messages for semantic recall
- 🟠 **GraphDB**: Stores structured information about the user — like their interests, behavior, and network

This approach gives agents the ability to:
- Remember facts over time
- Understand the user's profile
- Adapt responses dynamically to context and history

LangChain handles:
- ✅ Retrieval
- ✅ Prompt construction
- ✅ Context formatting  
...all under the hood.

---

## 💻 Let's See It in Action

Now let's walk through the code together.

We'll cover:
- How to initialize memory stores
- How to wire them into an agent
- And how the agent uses them to build intelligent, context-aware prompts in real time

Let's dive in!
