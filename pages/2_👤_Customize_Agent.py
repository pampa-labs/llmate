import streamlit as st
import tempfile
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

import llmate_config
llmate_config.general_config()
llmate_config.init_session_state()

def save_agent():
    st.session_state['sql_agent_prefix'] = st.session_state['prompt_editor']
    st.session_state['sql_agent'] = create_sql_agent(
        llm = st.session_state['llm'],
        toolkit=st.session_state['sql_toolkit'],
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        prefix=st.session_state['sql_agent_prefix']
    )

if st.session_state['openai_api_key'] != '':
    st.subheader("Customize the Agent Prompt")
    new_prompt = st.text_area("`SQL Agent Prompt`",
                                st.session_state['sql_agent_prefix'], 
                                height=500,
                                key='prompt_editor',
                                label_visibility='collapsed',
                                on_change=lambda: st.toast("Agent saved 🔥"))
    save_agent()
    with st.expander("View complete Agent prompt"):
        st.text(st.session_state['sql_agent'].agent.llm_chain.prompt.template)
else:
    st.error('Please load OpenAI API KEY', icon='🚨')