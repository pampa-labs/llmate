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
    # -------------------------------From main page------------------------------
    initial_variables['openai_model'] = 'gpt-3.5-turbo'
    initial_variables['uploaded_db'] = None
    initial_variables['db_path'] = 'example/Example_Chinook.db'
    initial_variables['db_name'] = 'Example_Chinook.db'

    # -------------------------------From Customize Database------------------------------
    initial_variables['sql_db'] = SQLDatabase.from_uri("sqlite:///" + initial_variables['db_path'])
    initial_variables['sample_rows_in_table_info'] = 2
    initial_variables['include_tables'] = initial_variables['sql_db'].get_table_names()
    initial_variables['table_names'] = initial_variables['sql_db'].get_table_names()

    #-------------------------------From Customize Agent------------------------------
    initial_variables['sql_agent_prefix'] = SQL_PREFIX
    initial_variables['sql_agent_suffix'] = SQL_FUNCTIONS_SUFFIX

    if  st.session_state.get('openai_api_key'):
        # -------------------------------From Customize Database------------------------------
        initial_variables['llm'] = ChatOpenAI(
            temperature=0, 
            verbose=True, 
            model=initial_variables['openai_model'],
            openai_api_key=st.session_state['openai_api_key'])
        initial_variables['sql_toolkit'] =  SQLDatabaseToolkit(db=initial_variables['sql_db'],
                                                            llm=initial_variables['llm']
                                                            )
        initial_variables['sql_agent'] = create_sql_agent(llm = initial_variables['llm'],
                                                        toolkit=initial_variables['sql_toolkit'],
                                                        verbose=True,
                                                        agent_type=AgentType.OPENAI_FUNCTIONS,
                                                        prefix=initial_variables['sql_agent_prefix'],
                                                        suffix=initial_variables['sql_agent_suffix']
                                                        )
        
    else:
        initial_variables['openai_api_key'] = ''
        
    for variable in initial_variables:
        if variable not in st.session_state:
            st.session_state[variable] = initial_variables[variable]