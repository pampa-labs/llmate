import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits.sql.prompt import SQL_PREFIX, SQL_FUNCTIONS_SUFFIX


import llmate_config
llmate_config.general_config()

def save_agent():
    st.session_state['sql_agent_prefix'] = st.session_state['prefix_editor']
    st.session_state['sql_agent_suffix'] = st.session_state['suffix_editor']
    st.session_state['sql_agent'] = create_sql_agent(
        llm = st.session_state['llm'],
        toolkit=st.session_state['sql_toolkit'],
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        prefix=st.session_state['sql_agent_prefix'],
        suffix=st.session_state['sql_agent_suffix']
    )
    st.toast("Agent saved 🔥")

if (st.session_state['openai_api_key'] != '') & (st.session_state['db_uri'] != ''):
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
else:
    st.error('Please load OpenAI API KEY and connect to a database', icon='🚨')