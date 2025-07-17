import streamlit as st
from chatbot import ask_bot

# --- Streamlit page config ---
st.set_page_config(
    page_title="BHC Global Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom Styling (Light theme, blue & grey) ---
st.markdown("""
    <style>
        body {
            background-color: white;
        }
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
        .chat-box {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            border-radius: 16px;
            padding: 14px;
            background-color: #f0f0f0;
            margin-bottom: 10px;
        }
        .user-msg {
            color: #0033A0;
            font-weight: 600;
        }
        .bot-msg {
            color: #333;
        }
        .avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            object-fit: cover;
            margin-top: 4px;
        }
        input[type=text] {
            border-radius: 12px;
            border: 1px solid #ccc;
            padding: 10px;
            width: 100%;
            margin-right: 8px;
        }
        .input-row {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .send-btn {
            background-color: #ADD8E6 !important;
            color: black !important;
            border-radius: 50%;
            padding: 8px 12px;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Intro Header ---
st.markdown("""
    <h3 style='color:#0033A0; margin-bottom:10px;'>🤖 BHC Global AI Assistant</h3>
    <p>Ask me anything about BHC Global’s services, products, careers, or mission.</p>
""", unsafe_allow_html=True)

# --- Session State Init ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "intro_shown" not in st.session_state:
    st.session_state.intro_shown = True
    st.session_state.chat_history.append(("🤖", "Hi, I’m Ava, your BHC Global AI Assistant. How can I help you today?"))

if "last_bot_prompt" not in st.session_state:
    st.session_state.last_bot_prompt = None

# --- Keywords to trigger PCAI fallback ---
powerconnect_keywords = {
    "pcai", "powerconnect", "powerconnect.ai", "powerconnectai.com", "powerconnectai"
}

def is_powerconnect_query(user_input):
    return any(keyword in user_input.lower().replace(" ", "") for keyword in powerconnect_keywords)

# --- Simple follow-up detection ---
followup_yes = {"yes", "yeah", "yup", "sure", "tell me more", "go on"}
followup_no = {"no", "nah", "no thanks"}

# --- Input field and icon ---
query = st.text_input("Type your question here:", key="chat_input", label_visibility="collapsed")

col1, col2 = st.columns([12, 1])
with col1:
    pass  # input already above
with col2:
    if st.button("➤", key="send", help="Send", use_container_width=True):
        st.session_state.submit_clicked = True
    else:
        st.session_state.submit_clicked = False

if query and (st.session_state.get("submit_clicked") or st.session_state.get("chat_input_submitted")):
    with st.spinner("Thinking..."):
        normalized = query.strip().lower()

        if normalized in followup_yes and st.session_state.last_bot_prompt:
            query = st.session_state.last_bot_prompt
        elif normalized in followup_no:
            response = "That's totally fine. Let me know if there's something else you'd like to explore."
            st.session_state.last_bot_prompt = None
        elif is_powerconnect_query(query):
            response = "PowerConnect.AI (PCAI) is part of BHC Global — we connect people with data through smart digital tools. Learn more at [powerconnect.ai](https://www.powerconnect.ai)"
            st.session_state.last_bot_prompt = None
        else:
            response = ask_bot(query)

            if "The text provided does not mention or define" in response or "The passage states" in response:
                response = "Hmm, I couldn’t find much on that — could you try rephrasing or giving me a bit more context?"
                st.session_state.last_bot_prompt = None
            elif "Would you like to know more" in response:
                st.session_state.last_bot_prompt = query
            else:
                st.session_state.last_bot_prompt = None

        # Save the conversation
        st.session_state.chat_history.append(("🧑‍💼", query))
        st.session_state.chat_history.append(("🤖", response))

# --- Render chat ---
for speaker, msg in st.session_state.chat_history:
    if speaker == "🧑‍💼":
        st.markdown(f"""
            <div class='chat-box'>
                <div class='user-msg'><strong>{speaker}</strong>: {msg}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='chat-box'>
                <img class='avatar' src='https://cdn.imgbin.com/24/14/3/3d-woman-avatar-stylized-cartoon-woman-avatar-with-glasses-knJAM2pV.jpg' alt='Ava avatar'/>
                <div class='bot-msg'>{msg}</div>
            </div>
        """, unsafe_allow_html=True)

# --- JS to trigger submit on Enter ---
st.markdown("""
    <script>
    const inputBox = window.parent.document.querySelector('input[data-testid="stTextInput"]');
    if (inputBox) {
        inputBox.addEventListener("keydown", function(e) {
            if (e.key === "Enter") {
                const btn = window.parent.document.querySelector('button[kind="primary"]');
                if (btn) btn.click();
            }
        });
    }
    </script>
""", unsafe_allow_html=True)
