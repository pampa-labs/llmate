import streamlit as st
import llmate_config

from utils import load_initial_state, load_initial_agent, update_model

load_initial_state()
llmate_config.general_config()
    
st.header("LLMate 🧉")

st.markdown(
    """
    This application is designed for customizing and evaluating a **LangChain SQL Agent**. 
    
    ---
    ### TODO - Refactor
    
    It consists of the following main modules: 

    1. 🔌 **Connect DB** - which allows you to select a dialect and connect to your own db
    2. 📄 **Customize Database** - which allows you to select which tables to use and change the descriptions.  
    3. 👤 **Customize Agent** - which allows you to customize your LLM agent according to your needs.  
    4. 🥃 **Add Few Shots** - whick allows you to add some concrete examples to help the agent answer complex questions
    5. ✅ **Test Agent** - which allows you to actually test the agent running queries on your DB.  
    6. 📊 **Evaluate Agent** - which allows you to evaluate the performance of your LLM agent.   
    7. 🤖 **Export Agent** - which allows you to fully recreate the Agent in your own solution.
    
    Let's start by setting up **OpenAI API KEY** and your **Database**. You can try the tool with the preloaded db or update your own.
"""
)

c1, c2 = st.columns([2,1])
with c1:
    st.session_state['api_key_input'] = st.text_input("`OpenAI Api Key`",
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
                                                   
if  st.session_state['openai_api_key']:
    masked_api_key = st.session_state['openai_api_key'][:3] + '******' + st.session_state['openai_api_key'][-3:]
    st.session_state['masked_api_key'] = masked_api_key
    st.success(f"Loaded OpenAI API Key: {st.session_state['masked_api_key']}")
    load_initial_agent()