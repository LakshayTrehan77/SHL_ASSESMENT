import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="SHL Assessment Recommendation System",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto"
)

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

st.sidebar.markdown(
    "<p><strong>Lakshay Trehan</strong><br>"
    "B.Tech CS Undergraduate at Indraprastha Institute of Information Technology Delhi (IIITD'2026)<br>"
    "Passionate Software Engineer 🚀 | Web Developer 💻<br>"
    "LLM Enthusiast 🤖 | AI & ML 🧠</p>",
    unsafe_allow_html=True
)

st.title("🔍 SHL Assessment Recommendation System")

query = st.text_area("Enter Job Description or Query:", placeholder="e.g., software engineer skills assessment")

if st.button("Get Recommendations"):
    if not query:
        st.warning("Please enter a query!")
    else:
        try:
            res = requests.post(
                "http://localhost:8000/recommend",
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            res.raise_for_status()
            assessments = res.json().get("recommended_assessments", [])

            if not assessments:
                st.warning("No recommendations found.")
            else:
                for a in assessments:
                    url = a.get("url", "#")
                    description = a.get("description", "No description available.")
                    adaptive_support = a.get("adaptive_support", "N/A")
                    remote_support = a.get("remote_support", "N/A")
                    duration = a.get("duration", "N/A")
                    # Handle test_type as a list or string
                    test_type = a.get("test_type", [])
                    if isinstance(test_type, str):
                        test_type = [test_type]  # Convert string to single-item list
                    test_type_str = ", ".join(test_type) if test_type else "N/A"
                    name = description[:50] + "..." if len(description) > 50 else description

                    st.markdown(f"### [**{name}**]({url})")
                    st.write(description)

                    df = pd.DataFrame({
                        "Adaptive Support": [adaptive_support],
                        "Remote Support": [remote_support],
                        "Duration (mins)": [duration],
                        "Test Type": [test_type_str]
                    })
                    st.table(df)
                    st.markdown("---")

        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            st.error(f"Network error occurred: {e}")
        except ValueError as e:
            st.error(f"Invalid response format: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")