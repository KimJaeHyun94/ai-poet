from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
import time
from streamlit_extras.buy_me_a_coffee import button
# load_dotenv()
# API_KEY = os.environ['OPENAI_API_KEY']

button(username="ru6300", floating=True, width=221)

#OpenAI KEY 입력 받기
API_KEY = st.text_input('OPEN_AI_API_KEY', type="password")

client = OpenAI(api_key=API_KEY)

# thread id 를 하나로 관리하기 위함
if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

thread_id = st.session_state.thread_id
assistant_id = "asst_nQIYlTb4mXsjELUubvGYhJxV"

thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

st.header("현진건 작가님과의 대화")

for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)

prompt = st.chat_input("물어보고 싶은 것을 입력하세요!")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,  # Corrected thread_id here
        role="user",
        content=prompt  # Use the actual prompt provided by the user
    )
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,  # Corrected thread_id here
        assistant_id=assistant_id,
    )   
    with st.spinner('응답 기다리는중...'):
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,  # Corrected thread_id here
                run_id=run.id
            )
            
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,  # Corrected thread_id here
    )
    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)
