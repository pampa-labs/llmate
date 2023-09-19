import streamlit as st
import llmate_config

from utils import load_initial_state, load_initial_agent, update_model, update_database_selection

load_initial_state()
llmate_config.general_config()
    
st.header("LLMate 🧉")

st.markdown(
    """
    This application is designed for customizing and evaluating a **LangChain SQL Agent**. 
    
    ---
    
    It consists of the following main modules: 

    1. 🔌 **DB Connection** - which allows you to select a database to use for evaluation
    2. 📄 **Customize Database** - which allows you to select the tables to be used and modify their descriptions.  
    3. 👤 **Customize Agent** - which allows you to customize your LLM agent prompt according to your needs.  
    4. 🥃 **Add Few Shots** - whick allows you to add some concrete examples to help the agent answer complex questions
    5. ✅ **Test Agent** - which allows you to actually test the agent running queries over the selected database.  
    6. 📊 **Evaluate Agent** - which allows you to evaluate the performance of your LLM agent.   
    7. 🤖 **Export Agent** - which allows you to fully recreate the Agent in your own solution.
    
    Let's start by setting up **OpenAI API KEY**
"""
)

c1, c2, c3 = st.columns([2,1,2])
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
with c3:
    st.session_state['database_selection'] = st.selectbox("Choose testing DB",
                                                          ['Chinook','Twitter'],
                                                          index=['Chinook','Twitter'].index(st.session_state['selected_database']),
                                                          on_change=update_database_selection,
                                                          key='database_selectbox')
                                                          
                                                          
if  st.session_state['openai_api_key']:
    masked_api_key = st.session_state['openai_api_key'][:3] + '******' + st.session_state['openai_api_key'][-3:]
    st.session_state['masked_api_key'] = masked_api_key
    st.success(f"Loaded OpenAI API Key: {st.session_state['masked_api_key']}")
    load_initial_agent()