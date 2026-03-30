import gradio as gr
from chat import get_response

def chat_fn(message, history):
    return get_response(message)

demo = gr.ChatInterface(fn=chat_fn, title="chatbot", description="chatbot with memory")

if __name__ == "__main__":
    demo.launch()