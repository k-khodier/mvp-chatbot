import streamlit as st
import os
from openai import OpenAI
import uuid  # für zufälligen Key

# OpenAI-Client initialisieren
client = OpenAI()

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title="KI-Projektideen-Chatbot", layout="centered")
st.title("KI-Projektideen-Chatbot")

st.markdown("""
Dieser Chatbot hilft dir, datengetriebene Projektideen im Bereich Simulation, Messtechnik oder KI zu validieren. 
Er kann Rückfragen stellen, analysieren und iterativ auf deine Antworten eingehen.
""")

# Session-State für Gesprächsverlauf initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": 
         "Du bist ein technischer Innovationsberater. Gib strukturierte Antworten und stelle Rückfragen, "
         "um Projektideen im Bereich Simulation, KI und Messtechnik zu bewerten und weiterzuentwickeln."}
    ]

# Anzeige der bisherigen Konversation
for msg in st.session_state.messages[1:]:  # system-prompt auslassen
    role = "Du" if msg["role"] == "user" else "Bot"
    st.markdown(f"**{role}:** {msg['content']}")

# Eingabefeld mit dynamischem Key, um es zu leeren
unique_key = str(uuid.uuid4())
user_input = st.text_input("Deine Eingabe", key=unique_key)

if st.button("Senden") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Bot denkt..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.6
        )
        bot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()
