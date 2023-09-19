import streamlit as st
import os

from langchain import SQLDatabase
from langchain.agents.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX, SQL_PREFIX
from langchain.chat_models import ChatOpenAI

from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType


def load_initial_state():
    if 'openai_api_key' not in st.session_state: 
        st.session_state['openai_api_key'] = (os.environ.get('OPENAI_API_KEY') or '')
    if 'openai_model' not in st.session_state:
        st.session_state['openai_model'] = 'gpt-3.5-turbo'
    if 'selected_database' not in st.session_state:
        st.session_state['selected_database'] = 'Chinook'
    if 'database_options' not in st.session_state:    
        st.session_state['database_options'] = {
                "Chinook": {
                    'db_uri': 'sqlite:///example/Chinook.db',
                    'few_shots': 'example/Chinook_few_shots.json',
                    'evaluation': 'example/Chinook_evaluation.json'
                },
                "Twitter": {
                    'db_uri': 'sqlite:///example/Twitter.sqlite',
                    'few_shots': 'example/Twitter_few_shots.json',
                    'evaluation': 'example/Twitter_evaluation.json'
                }
                }


def load_initial_agent():
    # if 'sql_agent' not in st.session_state:
    st.session_state['llm'] = ChatOpenAI(
            temperature=0, 
            verbose=True, 
            model=st.session_state['openai_model'],
            openai_api_key=st.session_state['openai_api_key'])
    st.session_state['db_uri'] = st.session_state['database_options'][st.session_state['selected_database']]['db_uri']
    st.session_state['sql_db'] = SQLDatabase.from_uri(st.session_state['db_uri'])
    st.session_state['sql_agent_prefix'] = SQL_PREFIX
    st.session_state['sql_agent_suffix'] = SQL_FUNCTIONS_SUFFIX
    st.session_state['few_shot_retriever'] = None
    st.session_state['extra_tools'] = []

    st.session_state['include_tables'] = st.session_state['sql_db'].get_table_names()
    st.session_state['table_names'] = st.session_state['sql_db'].get_table_names()
    tables_createtable_statement = st.session_state['sql_db'].get_table_info().split("CREATE TABLE")[1:]
    custom_table_info = {}

    for i in range(len(tables_createtable_statement)):
        custom_table_info[st.session_state['table_names'][i]] = "CREATE TABLE " + tables_createtable_statement[i]
    st.session_state['custom_table_info'] = custom_table_info

    st.session_state['sql_toolkit'] = SQLDatabaseToolkit(db=st.session_state['sql_db'],
                                                        llm=st.session_state['llm'],
                                                        custom_table_info=st.session_state['custom_table_info']
                                                        )
    update_agent()

def update_agent():
    st.session_state['sql_agent'] = create_sql_agent(
            llm = st.session_state['llm'],
            toolkit=st.session_state['sql_toolkit'],
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            prefix=st.session_state['sql_agent_prefix'],
            suffix=st.session_state['sql_agent_suffix'],
            extra_tools=st.session_state['extra_tools']
        )
def update_model():
    st.session_state['openai_model'] = st.session_state['model_selection']
    st.session_state['llm'] = ChatOpenAI(
            temperature=0, 
            verbose=True, 
            model=st.session_state['openai_model'],
            openai_api_key=st.session_state['openai_api_key']
            )
    
    st.toast(f"Updated model to {st.session_state['model_selection']}")

def update_database_selection():
    st.session_state['selected_database'] = st.session_state['database_selectbox']
    load_initial_agent()