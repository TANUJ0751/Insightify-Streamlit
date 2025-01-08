import requests
import streamlit as st
import pyperclip

# Load environment variables
APPLICATION_TOKEN = st.secrets["APP_TOKEN"]

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a429dc71-ad2c-4b98-b5b3-08779b951c6a"
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
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()

# Main function
def main():
    st.markdown(
        """
        <style>
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
    st.sidebar.title("**Insightify** : A Social Media Performance App")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "loading" not in st.session_state:
        st.session_state["loading"] = False
    if "current_message" not in st.session_state:
        st.session_state["current_message"] = ""

    # Show the spinner if loading is True
    if st.session_state["loading"]:
        spinner_html = """
        <div class="custom-spinner">
            <div class="spinner"></div>
        </div>
        """
        st.markdown(spinner_html, unsafe_allow_html=True)
        st.stop()  # Stops further execution until rerun

    # Input field for the user
    message = st.sidebar.text_area(
        "",
        value="",
        placeholder="How can we assist you today?",
    )

    # Button to send the query
    if st.sidebar.button("Generate", type="secondary"):
        if not message.strip():
            st.error("Please enter a message")
            return

        # Set loading state to True and save the current message
        st.session_state["loading"] = True
        st.session_state["current_message"] = message
        st.experimental_rerun()

    # Process the API response if a message is pending
    if st.session_state["current_message"] and not st.session_state["loading"]:
        try:
            response = run_flow(st.session_state["current_message"])
            response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]

            # Append user message and response to chat history
            st.session_state["messages"].append({"user": st.session_state["current_message"], "bot": response_text})

            # Clear the current message
            st.session_state["current_message"] = ""

        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            st.session_state["loading"] = False

    # Display chat history
    st.subheader("Chat History")
    bot_color = "#6af778"
    user_color = "#f4fa57"
    for chat in st.session_state["messages"]:
        st.markdown(f"<h5><strong style='color:{user_color};'>You:</strong> {chat['user']}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5><strong style='color:{bot_color};'>Bot:</strong> {chat['bot']}</h5>", unsafe_allow_html=True)
        st.divider()


if __name__ == "__main__":
    main()
