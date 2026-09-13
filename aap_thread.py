from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
import streamlit as st
import uuid


# generate unique uuid
def generate_thread_id():
    return str(uuid.uuid4())



## add a new thread_id to the config for each new session. This will allow us to have multiple conversations with the same chatbot without losing context. Each thread_id will have its own conversation history and state.
def add_thread():
    if 'thread_id' not in st.session_state
        st.session_state['thread_id'] = generate_thread_id()

st.title("Agentic AI Chatbot")
CONFIG = {'configurable': {'thread_id': 'thread_1'}}

# Creating session state , this is just for the purpose of storing the conversation history in the session state, so that it can be displayed in the chat interface. 
# The actual conversation state is managed by the LangGraph framework and is persisted using the MemorySaver checkpoint.

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# loading the conversatation history from the session state
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])



user_input = st.chat_input("Type your message here:")

if user_input:
    # User message
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant message container
    with st.chat_message("assistant"):
        def stream_response():
            for message_chunk, _ in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if message_chunk.content:
                    yield message_chunk.content

        AI_response = st.write_stream(stream_response())

    # Save assistant response
    st.session_state["message_history"].append(
        {"role": "assistant", "content": AI_response}
    )