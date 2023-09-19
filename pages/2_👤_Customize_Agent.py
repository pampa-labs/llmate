import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits.sql.prompt import SQL_PREFIX, SQL_FUNCTIONS_SUFFIX

import llmate_config
from utils import update_agent

llmate_config.general_config()

def save_agent():
    st.session_state['sql_agent_prefix'] = st.session_state['prefix_editor']
    st.session_state['sql_agent_suffix'] = st.session_state['suffix_editor']
    update_agent()
    st.toast("Agent saved 🔥")

if ('openai_api_key' not in st.session_state) or (st.session_state['openai_api_key'] == ''):
    st.error('Please load OpenAI API KEY and connect to a database', icon='🚨')
else:
    st.subheader("Customize the Agent Prompt")
    st.write("`Prefix:`")
    new_prompt = st.text_area("`Prefix:`",
                                st.session_state['sql_agent_prefix'], 
                                height=380,
                                key='prefix_editor',
                                label_visibility='collapsed',
                                # on_change=lambda: st.toast("Agent saved 🔥"),
                                on_change=save_agent)
    st.button("Reset to default prefix",
              disabled=(st.session_state['sql_agent_prefix']==SQL_PREFIX),
              on_click=lambda: setattr(st.session_state, 'sql_agent_prefix', SQL_PREFIX))
              
    st.write('`Suffix:`')
    new_prompt = st.text_area("`Suffix:`",
                                st.session_state['sql_agent_suffix'], 
                                height=40,
                                key='suffix_editor',
                                label_visibility='collapsed',
                                # on_change=lambda: st.toast("Agent saved 🔥"),
                                on_change=save_agent)
    st.button("Reset to default suffix",
              disabled=(st.session_state['sql_agent_suffix']==SQL_FUNCTIONS_SUFFIX),
              on_click=lambda: setattr(st.session_state, 'sql_agent_suffix', SQL_FUNCTIONS_SUFFIX))