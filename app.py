import streamlit as st
from chatbot import ask_bot

# Streamlit app configuration
st.set_page_config(page_title="BHC Global Chatbot", layout="wide")

# Title + description
st.title("🤖 BHC Global Chat Assistant")
st.markdown("Ask me anything about BHC Global's services, products, careers, or mission.")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
query = st.text_input("Type your question here:")

# On submit
if st.button("Ask") and query:
    with st.spinner("Thinking..."):
        response = ask_bot(query)
        st.session_state.chat_history.append((query, response))

# Show full conversation history
if st.session_state.chat_history:
    st.subheader("Chat History")
    for user_q, bot_a in reversed(st.session_state.chat_history):
        st.markdown(f"**🧑 You:** {user_q}")
        st.markdown(f"**🤖 Bot:** {bot_a}")
        st.markdown("---")
