import os
import random

import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX, SQL_PREFIX
from langchain.agents.agent_types import AgentType

# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SQLDatabase


def general_config():
    st.set_page_config(
        page_title="LLMate",
        page_icon="imgs/llmate.png",
        layout='wide'
    )

    hide_menu = '''
    <style>
       MainMenu {visibility: hidden;}
       footer {visibility: hidden;}
    </style>
    '''
    st.markdown(hide_menu, unsafe_allow_html=True)
    
    # twitters = ['https://twitter.com/fpingham', 'https://twitter.com/petrallilucas', 'https://twitter.com/manuelsoria_']
    # random.shuffle(twitters)
    
    footer = f"<style> footer:after {{content:'Made with 🧉';\
    visibility: visible; display: block; position: relative; padding: 0px; top: -20px;}}</style>"
    st.markdown(footer, unsafe_allow_html=True)


def init_session_state():

    initial_variables = {}
    # -------------------------------From Home ------------------------------
    # initial_variables['openai_api_key'] = ''
    # initial_variables['openai_model'] = 'gpt-3.5-turbo'
    # initial_variables['uploaded_db'] = None
    # initial_variables['db_path'] = 'example/Example_Chinook.db'
    # initial_variables['db_name'] = 'Example_Chinook.db'

    if 'openai_api_key' not in st.session_state: 
        st.session_state['openai_api_key'] = ''

    if 'openai_model' not in st.session_state:
        st.session_state['openai_model'] = 'gpt-3.5-turbo'

    if 'db_uri'not in st.session_state: 
        st.session_state['db_uri'] = ''

    if 'sql_db' not in st.session_state: 
        st.session_state['sql_db'] = ''

    # ------------------------------- From DB Connection --------------------
    # initial_variables['username'] = None
    # initial_variables['password'] = None
    # initial_variables['host'] = None
    # initial_variables['port'] = None
    # initial_variables['database_name'] = None
    # initial_variables['dialect'] = None
    # initial_variables['database_path'] = None
    # initial_variables['db_uri'] = ''

    # -------------------------------From Customize Database------------------------------
    if (st.session_state['openai_api_key'] != '') & (st.session_state['db_uri'] != ''):

        initial_variables['include_tables'] = st.session_state['sql_db'].get_table_names()

    
        initial_variables['table_names'] = st.session_state['sql_db'].get_table_names()


        initial_variables['sample_rows_in_table_info'] = 2


        initial_variables['sql_agent_prefix'] = SQL_PREFIX


        initial_variables['sql_agent_suffix'] = SQL_FUNCTIONS_SUFFIX


        initial_variables['llm'] = ChatOpenAI(
            temperature=0, 
            verbose=True, 
            model=st.session_state['openai_model'],
            openai_api_key=st.session_state['openai_api_key'])
        
        for variable in initial_variables:
            if variable not in st.session_state:
                st.session_state[variable] = initial_variables[variable]
        
        if 'sql_toolkit' not in st.session_state:
            st.session_state['sql_toolkit'] =  SQLDatabaseToolkit(
                db= st.session_state['sql_db'],
                llm=st.session_state['llm'])
        
        if 'sql_agent' not in st.session_state:
            st.session_state['sql_agent'] = create_sql_agent(llm = st.session_state['llm'],
                                                                toolkit=st.session_state['sql_toolkit'],
                                                                verbose=True,
                                                                agent_type=AgentType.OPENAI_FUNCTIONS,
                                                                prefix=st.session_state['sql_agent_prefix'],
                                                                suffix=st.session_state['sql_agent_suffix']
                                                                )


    