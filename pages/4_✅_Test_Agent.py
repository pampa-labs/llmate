import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler


import llmate_config
llmate_config.general_config()

if ('openai_api_key' not in st.session_state) or (st.session_state['openai_api_key'] == ''):
    st.error('Please load OpenAI API KEY and connect to a database', icon='🚨')
else:
    st.subheader("Test your Agent")

    user_query = st.text_input("Question:")
    st_callback = StreamlitCallbackHandler(st.container())
    if user_query:
        response = st.session_state['sql_agent'].run(user_query, callbacks=[st_callback])
        st.write(response)