import streamlit as st
import ollama

# Initialize Ollama client
def initialize_client():
    return ollama.Client(host='http://localhost:11434')  # Update if your server address is different

# Streamlit app
def main():
    st.title("Ollama Chat Interface")

    # Initialize client
    client = initialize_client()

    # Sidebar for model selection
    st.sidebar.header("Settings")
    model = st.sidebar.selectbox(
        "Choose a model:",
        ["llama3.1", "gemma2", "mistral-nemo", "mistral-large", "qwen2"]  # Update with available models
    )

    # User input
    st.header("Chat with the model")
    user_message = st.text_input("Enter your message:")
    if st.button("Send"):
        if user_message:
            # Request a response from the model
            response = client.chat(model=model, messages=[
                {'role': 'user', 'content': user_message}
            ])
            st.write("**Model Response:**")
            st.write(response['message']['content'])
        else:
            st.error("Please enter a message.")

if __name__ == "__main__":
    main()
