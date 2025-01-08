import requests
import streamlit as st

# Load environment variables
APPLICATION_TOKEN = st.secrets["APP_TOKEN"]

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a429dc71-ad2c-4b98-b5b3-08779b951c6a"
ENDPOINT = "social_media"

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
    response.raise_for_status()  # Raise error if the request fails
    return response.json()

# Main function
def main():
    st.sidebar.title("**Insightify** : A Social Media Performance App")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "loading" not in st.session_state:
        st.session_state["loading"] = False
    if "current_message" not in st.session_state:
        st.session_state["current_message"] = ""

    # Handle spinner and API call
    if st.session_state["loading"]:
        with st.spinner("Processing your request... Please wait."):
            try:
                response = run_flow(st.session_state["current_message"])
                response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                st.session_state["messages"].append({"user": st.session_state["current_message"], "bot": response_text})
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                st.session_state["loading"] = False
                st.session_state["current_message"] = ""

    # Input area
    message = st.sidebar.text_area(
        "Ask a question:",
        value="",
        placeholder="How can we assist you today?",
    )

    if st.sidebar.button("Generate"):
        if not message.strip():
            st.error("Please enter a valid message.")
        else:
            st.session_state["current_message"] = message
            st.session_state["loading"] = True
            st.experimental_rerun()

    # Display chat history
    st.subheader("Chat History")
    for chat in st.session_state["messages"]:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.divider()

if __name__ == "__main__":
    main()
