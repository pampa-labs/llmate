import streamlit as st
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import llmate_config

llmate_config.general_config()
# llmate_config.init_session_state()

def db_connection_variables():
    # List of session variable names
    default_values = {
        'username': None,
        'password': None,
        'host': 'localhost',
        'port': '3306',
        'database_name': None,
        'dialect': None
    }
    
    # Initialize session variables if they are not set
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

db_connection_variables()

st.header('🧉LLMate w/ own db conn')
dialects = ['sqlite', 'mysql', 'postgresql', 'oracle', 'mssql']

st.session_state.username = st.text_input('username')
st.session_state.password = st.text_input('password', type= "password")
st.session_state.host = st.text_input('host', "localhost") 
st.session_state.port = st.text_input('port', "3306")  # default port for MySQL
st.session_state.database_name = st.text_input('db name')
st.session_state.dialect = st.selectbox('Select a database dialect:', dialects)

#connect to db
if st.button('Connect to db'):
    try:
        st.session_state['db_uri'] = f"{st.session_state.dialect}://{st.session_state.username}:{st.session_state.password}@{st.session_state.host}:{st.session_state.port}/{st.session_state.database_name}"
        st.session_state['sql_db'] = SQLDatabase.from_uri(st.session_state['db_uri'])
        st.session_state['db_conn'] = st.session_state.database_name
        st.session_state['include_tables'] = st.session_state['sql_db'].get_table_names()
        st.session_state['table_names'] = st.session_state['sql_db'].get_table_names()
        st.success('Connected')
    except:
        st.error('Connection failed')

if 'db_conn' in st.session_state:
    st.success(f"Connected to {st.session_state['db_conn']}")
