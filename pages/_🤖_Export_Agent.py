# import base64
# import io
# import pickle

import json

import streamlit as st

import llmate_config

llmate_config.general_config()

if (st.session_state["openai_api_key"] != "") & (st.session_state["db_uri"] != ""):
    # st.session_state["sql_agent"].save_agent("agent.json")
    st.session_state["sql_agent"].agent = "openai_functions"
    print(type(st.session_state["sql_agent"].agent.dict()))
    # print(st.session_state["sql_agent"].agent.dict())
    # with open("agent.json", "w") as f:
    #     json.dump(st.session_state["sql_agent"].dict(), f, indent=4)

    # st.download_button(label="Download Agent", file_name="agent.json")
else:
    st.error("Please load OpenAI API KEY and a database", icon="🚨")
