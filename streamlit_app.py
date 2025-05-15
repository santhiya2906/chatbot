import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Cohere Chatbot", page_icon="🤖", layout="centered")

# Initialize session history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to fetch response from Cohere
def fetch_response_from_cohere(user_input, api_key):
    url = "https://api.cohere.ai/v1/chat"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": user_input,
        "chat_history": [],
        "model": "command-r-plus"  # Free tier model
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("text", "No response from Cohere.")
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except requests.RequestException as e:
        return f"⚠️ API connection failed: {str(e)}"

# Title and instructions
st.title("🤖 Free Cohere Chatbot")
st.markdown("Ask me anything! This chatbot is powered by Cohere's free Command-R+ model.")

# API key input
api_key = st.text_input("🔑 Enter your Cohere API Key", type="password")
if not api_key:
    st.warning("Please enter a valid API key to continue.")
    st.stop()

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 You:", key="user_input")
    send_button = st.form_submit_button("Send")

# Process and respond
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call Cohere API
    with st.spinner("🤖 Thinking..."):
        response = fetch_response_from_cohere(user_input, api_key)

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Sidebar info
with st.sidebar:
    st.header("📌 About This App")
    st.markdown("""
    This is a fully free chatbot using the Cohere API.  
    - No quota errors  
    - Easy to use  
    - Streamlit-powered  
    """)
    st.markdown("🔗 [Get a free Cohere API key](https://dashboard.cohere.com)")

