import streamlit as st
import ollama
import os

# Function to list available models
def list_models():
    return [
        'llama3.1', 'gemma2', 'mistral-nemo', 'mistral-large', 'qwen2',
        'deepseek-coder-v2', 'phi3', 'mistral', 'mixtral', 'codegemma',
        'command-r', 'command-r-plus', 'llava', 'llama3', 'gemma',
        'qwen', 'llama2', 'codellama', 'nomic-embed-text', 'dolphin-mixtral',
        'phi', 'llama2-uncensored'
    ]

# Function to load models
def load_model(model_name):
    os.system(f"ollama run {model_name} --download")
    st.success(f"Model '{model_name}' downloaded successfully.")

# Function to delete a model
def delete_model(model_name):
    os.system(f"ollama rm {model_name}")
    st.success(f"Model '{model_name}' deleted successfully.")

# Streamlit app layout
def main():
    st.title("Ollama Streamlit App")

    # Model management section
    st.sidebar.header("Model Management")
    models = list_models()
    
    # Download model
    with st.sidebar.form(key='download_model'):
        model_to_download = st.selectbox("Select model to download", models)
        st.form_submit_button("Download Model", on_click=load_model, args=(model_to_download,))
    
    # Delete model
    with st.sidebar.form(key='delete_model'):
        model_to_delete = st.selectbox("Select model to delete", models)
        st.form_submit_button("Delete Model", on_click=delete_model, args=(model_to_delete,))
    
    # Chat interface
    st.header("Chat with Model")
    model_name = st.selectbox("Select Model", models)
    custom_prompt = st.text_area("Custom System Prompt", "You are a helpful assistant.")
    chat_history = st.session_state.get('chat_history', [])
    
    user_input = st.text_input("Your message:")
    
    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            response = ollama.chat(model=model_name, messages=st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": response['message']['content']})
            st.experimental_rerun()
    
    st.subheader("Conversation")
    for message in st.session_state.get('chat_history', []):
        if message['role'] == 'user':
            st.write(f"**User:** {message['content']}")
        else:
            st.write(f"**Assistant:** {message['content']}")

if __name__ == "__main__":
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    main()
