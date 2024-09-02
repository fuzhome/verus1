import streamlit as st
import ollama
import json
import os

# Function to list models
def list_models():
    return ollama.list()

# Function to download a model
def download_model(model_name):
    ollama.pull(model_name)

# Function to delete a model
def delete_model(model_name):
    ollama.delete(model_name)

# Function to chat with a model
def chat_with_model(model_name, messages, system_prompt):
    if system_prompt:
        # Create a temporary model with the custom system prompt
        modelfile = f"""
        FROM {model_name}
        SYSTEM "{system_prompt}"
        """
        temp_model_name = f"{model_name}_custom"
        ollama.create(model=temp_model_name, modelfile=modelfile)
        model_name = temp_model_name

    response = ollama.chat(model=model_name, messages=messages)
    return response

# Streamlit app
def main():
    st.title("Ollama Chat Interface")

    # Sidebar for model management
    st.sidebar.header("Model Management")
    
    if st.sidebar.button("List Models"):
        models = list_models()
        st.sidebar.write("Available Models:")
        st.sidebar.write(models)

    selected_model = st.sidebar.selectbox("Select a Model", options=list_models())
    
    if st.sidebar.button("Download Selected Model"):
        download_model(selected_model)
        st.sidebar.write(f"Model {selected_model} downloaded.")
    
    if st.sidebar.button("Delete Selected Model"):
        delete_model(selected_model)
        st.sidebar.write(f"Model {selected_model} deleted.")

    # Main chat interface
    st.header("Chat with Model")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    with st.form(key='chat_form'):
        user_input = st.text_area("Enter your message:")
        system_prompt = st.text_area("Enter a custom system prompt (optional):")
        submit_button = st.form_submit_button(label='Send')
        
        if submit_button and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = chat_with_model(selected_model, st.session_state.messages, system_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response['message']['content']})
    
    # Display chat history
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")

if __name__ == "__main__":
    main()
