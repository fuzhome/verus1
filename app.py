import streamlit as st
import ollama
import io

# Function to handle the chat interaction
def chat_with_model(messages):
    response = ollama.chat(
        model='llama2-uncensored',
        messages=messages
    )
    return response['message']['content']

# Initialize Streamlit app
st.title("Chat with Llama2-Uncensored")

# State to store chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# User input
user_message = st.text_input("You:", "")

if st.button("Send") and user_message:
    # Add user message to chat history
    st.session_state.history.append({'role': 'user', 'content': user_message})
    
    # Get response from model
    bot_response = chat_with_model(st.session_state.history)
    
    # Add model response to chat history
    st.session_state.history.append({'role': 'assistant', 'content': bot_response})

# Display chat history
if st.session_state.history:
    for message in st.session_state.history:
        role = "You" if message['role'] == 'user' else "Assistant"
        st.write(f"**{role}:** {message['content']}")
