# Import libraries
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load environment variables from a .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model and get response
model = genai.GenerativeModel("gemini-1.5-flash-002")
chat = model.start_chat(history=[])

def get_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize streamlit app
st.set_page_config(page_title="Chatbot App")
st.header("Q&A Chatbot")
st.write("")
st.markdown("###### Have a question?  This friendly Q&A Chatbot provides a simple, conversational way to get the information you're looking for.")

# Initialize session state and query count for history
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []
if "query_count" not in st.session_state:
    st.session_state['query_count'] = 0

# Initialize user input
input = st.text_input("You: ", key="input")
submit = st.button("Ask the question")

def manage_query_count():
    """
    Manage query count and reset after a minute if limit is exceeded.
    """
    if st.session_state['query_count'] > 5:
        st.warning("You have reached the limit of 5 queries. Please try again later.")
        return
        # st.session_state['reset_time'] = time.time()
        # if 'reset_time' in st.session_state and time.time() - st.session_state['reset_time'] > 60:
        #     st.session_state['query_count'] = 0
        #     del st.session_state['reset_time']
    else:
        st.session_state['query_count'] += 1

def generate_response():
    """
    Handle user input and display chat history.
    """
    if submit and input:
        response = get_response(input)
        st.session_state.chat_history.append(("You", input))
        st.subheader("The Response is:")
        chunks = [chunk.text for chunk in response]
        full_response = ''.join(chunks)
        st.write(full_response)
        st.session_state.chat_history.append(("Bot", full_response))  
    

# Display chat history
def display_chat():
    """
    Show chat history.
    """
    st.subheader("Chat History:")
    for role, text in st.session_state.chat_history:
        st.write(f"{role}: {text}")



# Call Functions
manage_query_count()
generate_response()
display_chat()