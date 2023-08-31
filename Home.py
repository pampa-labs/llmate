import streamlit as st
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SQLDatabase
import llmate_config

llmate_config.general_config()
# llmate_config.init_session_state()

if 'openai_api_key' not in st.session_state: 
    st.session_state['openai_api_key'] = ''

if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

def update_model():
    st.session_state['openai_model'] = st.session_state['model_selection']
    st.session_state['llm'] = ChatOpenAI(
            temperature=0, 
            verbose=True, 
            model=st.session_state['openai_model'],
            openai_api_key=st.session_state['openai_api_key']
            )
    
    st.toast(f"Updated model to {st.session_state['model_selection']}")
    
st.header("LLMate 🧉")

st.markdown(
    """
    This application is designed for customizing and evaluating an LLM-to-SQL solution. 
    It consists of the following main modules: 

    1. 🔌 **Connect DB** - which allows you to select a dialect and connect to your own db
    2. 📄 **Customize Database** - which allows you to select which tables to use and change the descriptions.  
    3. 👤 **Customize Agent** - which allows you to customize your LLM agent according to your needs.  
    4. ✅ **Test Agent** - which allows you to actually test the agent running queries on your DB.  
    5. 📊 **Evaluate Agent** - which allows you to evaluate the performance of your LLM agent.   
    6. 🤖 **Export Agent** - which allows you to fully recreate the Agent in your own solution.
    
    Let's start by setting up **OpenAI API KEY** and your **Database**. You can try the tool with the preloaded db or update your own.
"""
)

c1, c2 = st.columns([2,1])
with c1:
    st.session_state['api_key_input'] = st.text_input("`OpenAI Api Key`",
                                                    type='password',
                                                    value=st.session_state['openai_api_key'])
with c2:
    st.session_state['openai_model_selection'] = st.radio("`OpenAI model`",
                                                        ("gpt-3.5-turbo", "gpt-4"),
                                                        index=("gpt-3.5-turbo", "gpt-4").index(st.session_state['openai_model']),
                                                        on_change=update_model,
                                                        key='model_selection'
                                                        )           
                                                   
st.session_state['openai_api_key'] = st.session_state['api_key_input']


if  st.session_state['openai_api_key']:
    masked_api_key = st.session_state['openai_api_key'][:3] + '******' + st.session_state['openai_api_key'][-3:]
    st.session_state['masked_api_key'] = masked_api_key
    st.success(f"Loaded OpenAI API Key: {st.session_state['masked_api_key']}")


# db = st.file_uploader("`Upload database as a .db file`",
#                         type="db",
#                         key='db_uploader',
#                         )

# if db is not None:
#     st.session_state['uploaded_db'] = db
#     st.session_state['db_name'] = st.session_state['uploaded_db'].name
#     tfile = tempfile.NamedTemporaryFile(delete=False) 
#     tfile.write(st.session_state['uploaded_db'].read())
#     tfile.close()
#     st.session_state['db_path'] = tfile.name
#     st.session_state['sql_db'] = SQLDatabase.from_uri("sqlite:///" + st.session_state['db_path'])
#     st.session_state['sample_rows_in_table_info'] = 2
#     st.session_state['include_tables'] = st.session_state['sql_db'].get_table_names()
#     st.session_state['table_names'] = st.session_state['sql_db'].get_table_names()


# if st.session_state['uploaded_db'] is not None:
#     st.success(f"Loaded Database: {st.session_state['db_name']}")
# else:
#     st.info(f"Pre-Loaded Database: {st.session_state['db_name']}")



# footer = f"<style> footer:after {{content:'version ';\
#        visibility: visible; display: block; position: relative; padding: 0px; top: -20px;}}</style>"
# st.markdown(footer, unsafe_allow_html=True)