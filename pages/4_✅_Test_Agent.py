import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler


import llmate_config
llmate_config.general_config()
llmate_config.init_session_state()

if (st.session_state['openai_api_key'] != '') & (st.session_state['db_uri'] != ''):
    st.subheader("Test your Agent")

    user_query = st.text_input("Question:")
    st_callback = StreamlitCallbackHandler(st.container())
    if user_query:
        response = st.session_state['sql_agent'].run(user_query, callbacks=[st_callback])
        st.write(response)
else:
    st.error('Please load OpenAI API KEY and a database', icon='🚨')