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