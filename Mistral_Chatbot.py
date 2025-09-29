import gradio as gr
from mistralai import Mistral

api_key = "kw73FMj4V7HsZQ91CHei3N6TNfEN8ARn"
model = "mistral-small-latest"

client = Mistral(api_key=api_key)

def chat_with_mistral(message, history):
    messages = []
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})
    
    try:
        response = client.chat.complete(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

gr.ChatInterface(
    fn=chat_with_mistral,
    title="Mistral Chatbot",
    description="Ask anything to Mistral!"
).launch()
