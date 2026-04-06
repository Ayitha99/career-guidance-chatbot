# app.py
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from groq import Groq

# Configure the Groq API
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

# Configure Streamlit page
st.set_page_config(page_title="Career Guidance Chatbot", layout="centered")
st.title("🎓 Career Guidance Chatbot")
st.subheader("Your AI assistant for career advice, skills, and learning roadmaps")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I'm your career guidance assistant. I can help you choose careers, suggest skills, and guide your learning path. What would you like to explore today?"
        }
    ]

def display_messages():
    """Display all messages in the chat history"""
    for msg in st.session_state.messages:
        author = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(author):
            st.write(msg["content"])

def friendly_wrap(raw_text):
    """Add a friendly tone to AI responses"""
    return (
        "Great question! 🎓\n\n"
        f"{raw_text.strip()}\n\n"
        "Do you want a roadmap, skills list, or job suggestions for this?"
    )

# Display existing messages
display_messages()

# 🔥 Quick option buttons
col1, col2, col3 = st.columns(3)

if col1.button("💻 Software Jobs"):
    st.session_state.messages.append({"role": "user", "content": "Guide me to become a software engineer"})
    st.rerun()

if col2.button("🤖 AI / Data Science"):
    st.session_state.messages.append({"role": "user", "content": "How to start a career in AI and data science?"})
    st.rerun()

if col3.button("🏛️ Government Jobs"):
    st.session_state.messages.append({"role": "user", "content": "Best government job options in India"})
    st.rerun()

# Handle user input
prompt = st.chat_input("Ask about careers, skills, jobs, or roadmaps...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

# If last message is user → generate response
if st.session_state.messages[-1]["role"] == "user":

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("🤔 Thinking...")

        try:
            # 🔥 IMPORTANT: use full chat history
            messages = [
                {
                    "role": "system",
                    "content": "You are a career guidance expert. Help students and professionals choose careers, suggest skills, provide roadmaps, and give practical advice in simple language."
                }
            ] + st.session_state.messages

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=messages
            )

            answer = response.choices[0].message.content
            friendly_answer = friendly_wrap(answer)

        except Exception as e:
            friendly_answer = f"Error: {e}"

        placeholder.write(friendly_answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": friendly_answer
        })

    st.rerun()