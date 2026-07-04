# frontend/streamlit_app.py

import json
from pathlib import Path
import streamlit as st
import requests
import sys

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
        st.warning("Please enter both an event description, bio and your interests.")

# --- DISPLAY RESULTS ---
if "suggestions" in st.session_state:
    st.subheader("🎯 Extracted Themes")
    st.write(st.session_state["topics"])

    st.subheader("💬 Conversation Starters")
    for i, suggestion in enumerate(st.session_state["suggestions"]):
        st.markdown(f"- {suggestion}")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("👍", key=f"like_{i}"):
                requests.post(f"{BASE_URL}/feedback", params={"suggestion": suggestion, "action": "like"})
                st.success("Thanks for the feedback!")
        with col2:
            if st.button("👎", key=f"dislike_{i}"):
                requests.post(f"{BASE_URL}/feedback", params={"suggestion": suggestion, "action": "dislike"})
                st.info("Feedback noted.")


#--- FACT CHECK SECTION ---
st.markdown("---")
st.subheader("🔍 Quick Fact-Check")

query = st.text_input("Enter a topic to fact-check:")
if st.button("Fact-Check"):
    if query:
        response = requests.post(f"{BASE_URL}/fact-check", json={"query": query})
        if response.status_code == 200:
            st.success(response.json()["summary"])
        else:
            st.error("Failed to fetch fact-check information.")
    else:
        st.warning("Please enter a topic to fact-check.")


# --- CONVERSATION HISTORY ---

st.markdown("---")
st.subheader("📜 View Previous Conversations")

if st.button("Show History"):
    history_path = Path("history.json")
    if history_path.exists():
        with open(history_path, "r") as f:
            history = json.load(f)
        for item in reversed(history[-5:]):  # show latest 5
            st.markdown(f"**🕐 {item['timestamp']}**")
            st.write("**Event:**", item["description"])
            st.write("**Interests:**", ", ".join(item["interests"]))
            st.write("**Topics:**", ", ".join(item["topics"]))
            st.write("**Suggestions:**")
            for s in item["suggestions"]:
                st.markdown(f"- {s}")
            st.markdown("---")
    else:
        st.info("No history found yet.")

st.markdown("---")
st.subheader("📁View Feedback History")

if st.button("Show Feedback History"):
    feedback_path = Path("feedback.json")
    if feedback_path.exists():
        with open(feedback_path, "r") as f:
            feedback_data = json.load(f)
        for item in reversed(feedback_data[-10:]):  # show latest 10
            icon= "👍🏻" if item["feedback"] == "like" else "👎🏻"
            st.markdown(f"{icon} **{item['suggestion']}**")
            st.caption(f"🕐 {item['timestamp']}")
            st.markdown("---")
    else:
        st.info("No feedback history found yet.")