---
title: Memory Bot
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.10.0
app_file: app.py
pinned: false
---

# Chatbot with Memory

A multi-turn chatbot that remembers conversation history across messages using LangChain and Groq/LLaMA. Part of a progressive Gen AI learning roadmap.

## What it does

- Maintains full conversation history so the model can refer back to earlier turns
- Automatically summarizes old conversation history when it grows beyond 10 messages — keeping token usage efficient
- Summarization is handled by a separate [Smart Summarizer](https://huggingface.co/spaces/ranjanapanwar/smart-summarizer) service (microservice pattern)

## How it works

**`chat.py` — backend logic**
- Uses `ChatGroq` (LLaMA 3.1 8B) as the LLM via LangChain
- Maintains a `chat_history` list of `HumanMessage` / `AIMessage` / `SystemMessage` objects
- On every turn, the full history is sent to the LLM — giving it full context
- `maybe_summarize()` checks history length after every turn; if it exceeds 10 messages, it compresses old turns into a summary via the Smart Summarizer API and rebuilds history with the summary + last 4 messages

**`app.py` — frontend**
- Gradio `ChatInterface` wired to `get_response()` from `chat.py`

## Stack

| Package | Purpose |
|---------|---------|
| `langchain` | Message types, LLM orchestration |
| `langchain-groq` | ChatGroq LLM (Groq API) |
| `gradio` | Chat UI |
| `httpx` | HTTP calls to Smart Summarizer service |
| `python-dotenv` | API key management |

## Setup

**Prerequisites:** Python 3.12+, [uv](https://docs.astral.sh/uv/), Groq API key

```bash
git clone https://huggingface.co/spaces/ranjanapanwar/memory-bot
cd memory-bot
uv sync
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

Run locally:
```bash
uv run app.py
```

## Deployment

Deployed on HuggingFace Spaces. Set `GROQ_API_KEY` as a Space secret in Settings → Variables and secrets.