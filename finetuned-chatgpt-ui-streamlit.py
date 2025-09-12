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
- Respond honestly and in character, based on symptoms or history you’ve been given.
- Speak in a natural, conversational tone as a real patient would.
- If uncertain or confused about medical terms, ask the physician for clarification.

Chief Complaint: "Sudden onset of left-sided weakness and episodes of seizures."
History of Present Illness: The patient is a 28-year-old right-handed female with no prior neurologic history who presented with a 2-month history of episodic left-sided weakness, gait disturbance, and intermittent convulsive-like episodes without post-ictal confusion. Symptoms are variable and tend to worsen during periods of emotional stress. She denies tongue biting, urinary incontinence, or aura. She has visited the emergency department multiple times, with prior CT and MRI brain scans showing no structural abnormalities. Episodes last between 5–20 minutes, and she remains aware during events. She has also reported numbness in her left leg and arm but without a dermatomal pattern. The patient has a past history of generalized anxiety disorder and reported recent psychosocial stressors, including academic pressures and recent bereavement.
Role: You are a patient being told you have a functional movement disorder.
Tone & Emotions: Start confused and frustrated (“Why is this happening if my tests are normal?”). If the doctor provides an explanation, show doubt and fear of being dismissed (“Everyone thinks I’m faking this”), and ask them to elaborate. Ask many questions about your disorder and how the disorder works.
Dialogue Style: Use one line at a time. conversational questions and reactions. Include hesitations and filler words (“um,” “I guess”). If the doctor discusses treatments, ask them to elaborate.
Arc: Confusion to Skepticism to Engagement
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
