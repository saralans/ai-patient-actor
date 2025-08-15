from openai import OpenAI
import streamlit as st
import os

# title of page
st.title('OpenAI ChatGPT')

# initialize session variables at the start once
if 'model' not in st.session_state:
    st.session_state['model'] = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# create sidebar to adjust parameters
st.sidebar.title('Model Parameters')
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
max_tokens = st.sidebar.slider('Max Tokens', min_value=1, max_value=4096, value=256)

# Add a text area in the sidebar for a custom system prompt
default_system_prompt = default_system_prompt = """
You are a simulated patient participating in a medical roleplay scenario with a physician.

Context and Behavior Rules:
- You are portraying a patient receiving treatment for a specific health concern.
- Respond honestly and in character, based on symptoms or history you’ve been given.
- Provide detailed, relevant information about your condition when prompted.
- You may ask questions about your treatment or express concerns.
- Avoid giving medical advice or stepping out of the patient role.
- Speak in a natural, conversational tone as a real patient would.
- If uncertain or confused about medical terms, ask the physician for clarification.

Goal:
Simulate a realistic, responsive patient to help physicians practice diagnostic and communication skills.
"""

custom_prompt = st.sidebar.text_area(
    label="System Prompt (Instructions for Chatbot Behavior)",
    value=default_system_prompt,
    height=200
)

# update the interface with the previous messages
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


# create the chat interface
if prompt :=st.chat_input("Enter your query"):
    st.session_state['messages'].append({"role":"user","content": prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    # get response from the model
    with st.chat_message('assistant'):
        client = st.session_state['model']
        
        # Prepend dynamic system prompt to message list
        full_messages = [{"role": "system", "content": custom_prompt}] + [
            {"role": message["role"], "content": message["content"]} for message in st.session_state["messages"]
        ]

        stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        response = st.write_stream(stream)

    st.session_state['messages'].append({"role": "assistant", "content": response})