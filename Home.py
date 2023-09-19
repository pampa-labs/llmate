import streamlit as st
import llmate_config

from utils import load_initial_state, load_initial_agent, update_model, update_database_selection

load_initial_state()
llmate_config.general_config()
    
st.header("LLMate 🧉")

st.markdown(
    """
    The **first playground** for optimizing and evaluating a **LangChain SQL Agent** in order to:
    
    - Improve **accuracy** 🎯
    - Reduce **cost** 💰
    
    ---
    Available modules:

    1. **Customize Database** - select the tables to be used and modify their descriptions 
    2. **Customize Agent** - customize your LLM agent prompt according to your needs
    3. **Add Few Shots** - provide `question-answer` examples to help the agent answer complex questions
    4. **Test Agent** - test the agent running queries over the selected database  
    5. **Evaluate Agent** - evaluate the performance of your LLM agent 
    6. **Export Agent** - export the agent to fully recreate it in your own solution
    
    Let's start by setting up your **OpenAI API Key** and choosing your **Testing Database**
"""
)

c1, c2, c3 = st.columns([2,1,2])
with c1:
    st.session_state['api_key_input'] = st.text_input("`OpenAI API Key`",
                                                    type='password',
                                                    value=st.session_state['openai_api_key'])
    st.session_state['openai_api_key'] = st.session_state['api_key_input']
with c2:
    st.session_state['openai_model_selection'] = st.radio("`OpenAI model`",
                                                        ("gpt-3.5-turbo", "gpt-4"),
                                                        index=("gpt-3.5-turbo", "gpt-4").index(st.session_state['openai_model']),
                                                        on_change=update_model,
                                                        key='model_selection'
                                                        )           
with c3:
    st.session_state['database_selection'] = st.selectbox("`Testing Database`",
                                                          ['Chinook','Twitter'],
                                                          index=['Chinook','Twitter'].index(st.session_state['selected_database']),
                                                          on_change=update_database_selection,
                                                          key='database_selectbox')
                                                          
                                                          
if  st.session_state['openai_api_key']:
    masked_api_key = st.session_state['openai_api_key'][:3] + '******' + st.session_state['openai_api_key'][-3:]
    st.session_state['masked_api_key'] = masked_api_key
    st.success(f"Loaded OpenAI API Key: {st.session_state['masked_api_key']}")
    load_initial_agent()