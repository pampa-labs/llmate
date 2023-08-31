import streamlit as st
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from streamlit_extras.grid import grid

import llmate_config

llmate_config.general_config()
llmate_config.init_session_state()

# if 'db_uri'not in st.session_state: 
#     st.session_state['db_uri'] = ''


st.header('LLMate 🧉')
dialects = ['sqlite', 'mysql', 'postgresql', 'oracle', 'mssql']

my_grid = grid(2, 4, 1, 1, vertical_align="bottom")

st.session_state.username = my_grid.text_input('username')
st.session_state.password = my_grid.text_input('password', type= "password")
st.session_state.host = my_grid.text_input('host', "localhost") 
st.session_state.port = my_grid.text_input('port', "3306")  # default port for MySQL
st.session_state.database_name = my_grid.text_input('db name')
st.session_state.dialect = my_grid.selectbox('Select a database dialect:', dialects)
st.session_state.database_path = st.text_input('Path to SQLite database file')

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    if st.button('Connect to db', use_container_width=True):
        try:
            if st.session_state.dialect == 'sqlite':
                st.session_state['db_uri'] = f"sqlite:///{st.session_state.database_path}"
                st.session_state['db_conn'] = st.session_state.database_path
            else:
                st.session_state['db_uri'] = f"{st.session_state.dialect}://{st.session_state.username}:{st.session_state.password}@{st.session_state.host}:{st.session_state.port}/{st.session_state.database_name}"
                st.session_state['db_conn'] = st.session_state.database_name

            st.session_state['sql_db'] = SQLDatabase.from_uri(st.session_state['db_uri'])
            st.success(f"Connected to {st.session_state['db_conn']}")

        except:

            st.error('Connection failed')

with col3:
    st.write(' ')


