import streamlit as st
import requests
import pandas as pd

# ─── API Setup ─────────────────────────────────────────────
API_URL = "http://localhost:8000/api/recommend/"
API_KEY = "rytO5BugHWdKUlXNvDTY78ZD7yXo42AJgnTofmaLokQ"  # Replace with your actual key

HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

# ─── Streamlit Page Config ────────────────────────────────
st.set_page_config(
    page_title="SHL Assessment Recommendation System",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto"
)

# ─── Custom Styling ───────────────────────────────────────
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stMarkdown table {
        font-size: 18px;
        color: #fafafa;
    }
    .stMarkdown td, .stMarkdown th {
        padding: 8px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        font-size: 18px;
    }
    .stButton>button {
        font-size: 18px;
    }
    .sidebar-content p {
        font-size: 32px;
        color: #fafafa;
        text-align: center;
        line-height: 1.4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ─── Sidebar Branding ─────────────────────────────────────
st.sidebar.markdown(
    "<p><strong>Lakshay Trehan</strong><br>"
    "B.Tech CS Undergraduate at Indraprastha Institute of Information Technology Delhi (IIITD'2026)<br>"
    "Passionate Software Engineer 🚀 | Web Developer 💻<br>"
    "LLM Enthusiast 🤖 | AI & ML 🧠</p>",
    unsafe_allow_html=True
)

# ─── Main App ──────────────────────────────────────────────
st.title("🔍 SHL Assessment Recommendation System")

query = st.text_area("Enter Job Description or Query:")

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a query!")
    else:
        try:
            res = requests.post(
                API_URL,
                json={"query": query},
                headers=HEADERS
            )

            if res.status_code != 200:
                st.error(f"Error {res.status_code}: {res.text}")
            else:
                assessments = res.json().get("recommended_assessments", [])

                if not assessments:
                    st.warning("No recommendations found.")
                else:
                    for a in assessments:
                        # Extract flat fields
                        name             = a.get("name", "Unnamed Assessment")
                        url              = a.get("url", "#")
                        description      = a.get("description", "No description provided.")
                        adaptive_support = a.get("adaptive_support", "N/A")
                        remote_support   = a.get("remote_support", "N/A")
                        duration         = a.get("duration", "N/A")
                        test_types       = a.get("test_type", [])

                        test_type_str = ", ".join(test_types) if isinstance(test_types, list) else test_types

                        # Display result
                        st.markdown(f"### [🔗 {name}]({url})")
                        st.write(description)

                        df = pd.DataFrame({
                            "Adaptive Support":  [adaptive_support],
                            "Remote Support":    [remote_support],
                            "Duration (mins)":   [duration],
                            "Test Types":        [test_type_str]
                        })
                        st.table(df)
                        st.markdown("---")

        except Exception as e:
            st.error(f"An error occurred: {e}")
