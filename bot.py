import gradio as gr
import openai, config

openai.api_key = config.OPENAI_API_KEY

model_engine = "text-davinci-002"
history = []

def generate_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def chatbot_interface(You):
    global history
    
    # Add role and content to the message
    message = f"You: {You}"
    prompt = message + "\nChatGPT: "
    
    # Add the message to the history
    history.append(message)
    
    # Generate the response
    response = generate_response(prompt)
    
    # Add the response to the history
    history.append("ChatGPT: " + response)
    
    # Combine the history into a list of question-answer pairs
    qa_pairs = []
    for i in range(0, len(history), 2):
        qa_pairs.append((history[i], history[i+1]))
    
    # Combine the question-answer pairs into a single string and return it
    history_str = "\n\n".join([f"{qa[0]}\n{qa[1]}" for qa in qa_pairs])
    return history_str


chatbot = gr.Interface(fn=chatbot_interface, 
                       inputs=gr.inputs.Textbox("You"), 
                       outputs=gr.outputs.Textbox(),
                       title="OpenAI Chatbot")

chatbot.launch()
