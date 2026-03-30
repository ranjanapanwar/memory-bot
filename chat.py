from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os
import httpx

load_dotenv()
key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=key)
chat_history = [SystemMessage("You are a helpful assistant.")]

def get_response(user_message):
    chat_history.append(HumanMessage(content=user_message))
    response = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    maybe_summarize()
    return response.content

def maybe_summarize():

    messages_count = len(chat_history) - 1

    if messages_count <= 10:
        return
    
    old_messages = chat_history[1:-4]
    recent_messages = chat_history[-4:]

    text = ""
    for message in old_messages:
        if isinstance(message, HumanMessage):
            text += "Human: " + message.content + "\n"
        elif isinstance(message, AIMessage):
            text += "AI: " + message.content + "\n"

    response = httpx.post("https://ranjanapanwar-smart-summarizer.hf.space/summarize-sync", json = {"text": text})

    summary = response.json()["summary"]

    chat_history.clear()
    chat_history.append(SystemMessage("You are a helpful assistant."))
    chat_history.append(SystemMessage("Summary of earlier conversation: " + summary))
    chat_history.extend(recent_messages)





