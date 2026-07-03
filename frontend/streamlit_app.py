# frontend/streamlit_app.py

import streamlit as st
import requests

# Backend base URL
BASE_URL = "http://127.0.0.1:8000"

st.title("🤝 Personalized Networking Assistant")
st.markdown("Generate conversation starters for networking events based on your interests.")

# --- INPUT SECTION ---
event_description = st.text_area("📝 Enter Event Description")
user_bio = st.text_area("🙋 Your Bio (a few sentences about yourself)")
user_interests = st.text_input("🎯 Your Interests (comma-separated)")


# --- GENERATE SECTION ---
if st.button("Generate Conversation Starters"):
    if event_description and user_interests:
        payload = {
            "description": event_description,
            "bio": user_bio,
            "interests": [i.strip() for i in user_interests.split(",")]
        }

        response = requests.post(f"{BASE_URL}/generate-conversation", json=payload)

        if response.status_code == 200:
            data = response.json()
            # Store results in session state so they persist after the button click
            st.session_state["topics"] = data["topics"]
            st.session_state["facts"] = data["facts"]
            st.session_state["suggestions"] = data["suggestions"]
        else:
            st.error("Failed to generate conversation starters.")
    else:
        st.warning("Please enter both an event description and your interests.")

# --- DISPLAY RESULTS ---
if "suggestions" in st.session_state:
    st.subheader("🎯 Extracted Themes")
    st.write(st.session_state["topics"])

    st.subheader("💬 Conversation Starters")
    for i, suggestion in enumerate(st.session_state["suggestions"]):
        st.markdown(f"- {suggestion}")