import requests
import streamlit as st
import pyperclip
import os
from PIL import Image

APPLICATION_TOKEN = st.secrets["APP_TOKEN"]
ENDPOINT = "social_media"
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a429dc71-ad2c-4b98-b5b3-08779b951c6a"
FLOW_ID = "b2965fbd-2779-4c01-b07d-3961555143c6"
ENDPOINT = "social_media"

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.markdown(
        """
        <style>
        .stButton>button:hover {
            background-color: #1b0e4a; 
            color: white; 
            border-color: #f4fa57;
        }
        .stButton>button:active {
        border-color: white;  
        color: white;  
        }
        .stButton{
        border-color: white;  
        color: white;  
        }
        
        .stApp {
            background-color: #1b0e4a; 
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            flex-direction: column;
        }
        
        [data-testid="stSidebar"] {
            background-color: #302a47; 
        }
        header {
            background-color: #1b0e4a !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.title(''' **Insightify** : A Social Media Performance App ''')
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""

    message = st.sidebar.text_area(
        "",
        value=st.session_state["input_text"],
        placeholder="How can we assist you today?",
        key="input_text",
    )

    if st.sidebar.button("Generate", icon=":material/send:", type="secondary"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            assets_folder = os.path.join(current_dir, "Assets")
            gif_path = os.path.join(assets_folder, "spinner.gif")
            gif_html = f'<img src="{gif_path}" width="100%">'
            st.markdown(gif_html, unsafe_allow_html=True)

            gif = Image.open(gif_path)
            spinner = st.image(gif, caption="Loading...", use_column_width=True)

            response = run_flow(message)
            response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]

            st.session_state["messages"].append({"user": message, "bot": response_text})

            spinner.empty()

        except Exception as e:
            st.error(str(e))

    st.subheader("Chat History")
    st.write("--------")
    bot_color = '#6af778'
    user_color = '#f4fa57'
    for chat in st.session_state["messages"]:
        st.markdown(f"<h5><strong style='color:{user_color};'>You:</strong> {chat['user']}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5><strong style='color:{bot_color};'>Bot:</strong> {chat['bot']}</h5>", unsafe_allow_html=True)
        st.divider()

if __name__ == "__main__":
    main()
