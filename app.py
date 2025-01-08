import requests
import streamlit as st
import pyperclip

# Load environment variables

# Load API key from environment variable
APPLICATION_TOKEN = st.secrets["APP_TOKEN"]

ENDPOINT = "analysis"
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a429dc71-ad2c-4b98-b5b3-08779b951c6"
FLOW_ID = "b2965fbd-2779-4c01-b07d-3961555143c6"
ENDPOINT = "social_media"  # The endpoint name of the flow

# Function to run the flow
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

# Main function
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
            border-color: white;  /* Border color after clicking */
            color: white;  /* Text color after clicking */
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
        .custom-spinner {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: rgba(0, 0, 0, 0.6);
            z-index: 9999;
        }
        .spinner {
            border: 16px solid #f3f3f3;
            border-top: 16px solid #1b0e4a;
            border-radius: 50%;
            width: 120px;
            height: 120px;
            animation: spin 2s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Spinner state in session
    if "show_spinner" not in st.session_state:
        st.session_state["show_spinner"] = False

    # Show spinner if active
    if st.session_state["show_spinner"]:
        st.markdown(
            """
            <div class="custom-spinner">
                <div class="spinner"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.sidebar.title("**Insightify** : A Social Media Performance App")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""

    # Input field for the user
    message = st.sidebar.text_area(
        "",
        value=st.session_state["input_text"],
        placeholder="How can we assist you today?",
        key="input_text",  # Link the input to session state
    )

    # Button to send the query
    if st.sidebar.button("Generate", icon=":material/send:", type="secondary"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            # Show spinner
            st.session_state["show_spinner"] = True
            st.experimental_rerun()

            # Run the API call
            response = run_flow(message)
            response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]

            # Append user message and response to chat history
            st.session_state["messages"].append({"user": message, "bot": response_text})

        except Exception as e:
            st.error(str(e))
        finally:
            # Hide spinner
            st.session_state["show_spinner"] = False
            st.experimental_rerun()

    # Display chat history
    st.subheader("Chat History")
    st.write("--------")
    bot_color = "#6af778"
    user_color = "#f4fa57"
    for chat in st.session_state["messages"]:
        st.markdown(f"<h5 ><strong style='color:{user_color};'>You:</strong> {chat['user']}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5><strong style='color:{bot_color};'>Bot:</strong> {chat['bot']}</h5>", unsafe_allow_html=True)
        st.divider()


if __name__ == "__main__":
    main()
