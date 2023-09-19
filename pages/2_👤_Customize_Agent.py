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
    st.markdown(
        """
        **Why customize the Agent's prompt? 🤔**

        Imagine giving a student a clear, concise essay prompt versus a vague, broad one. With clear instructions, the student knows exactly what's expected and can deliver a more thoughtful, accurate response. Similarly, when you customize the Agent's prompt, you're guiding its thought process.

        By personalizing the prompt, you:

        1. **Direct the Conversation**: It's like pointing the Agent to the exact topic or area you want to discuss.
        2. **Ensure Relevance**: Make sure the Agent's response aligns closely with what you're looking for.
        3. **Optimize Performance**: Like providing a student with the right tools, a clear prompt helps the Agent give the best possible answer.
        
        Crafting the right prompt is an art, and a key to unlocking the Agent's potential 🗝️. It's your way of setting the stage for a meaningful interaction. So, always invest a bit of time to refine and focus your prompts!

        """
    )

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