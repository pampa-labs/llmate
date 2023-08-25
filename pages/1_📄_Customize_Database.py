import streamlit as st

from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_toolkits.sql.prompt import SQL_PREFIX

import llmate_config
llmate_config.general_config()
llmate_config.init_session_state()


if 'custom_table_info' not in st.session_state:
        tables_createtable_statement = st.session_state['sql_db'].get_table_info().split("CREATE TABLE")[1:]
        custom_table_info = {}

        for i in range(len(tables_createtable_statement)):
            custom_table_info[st.session_state['table_names'][i]] = "CREATE TABLE " + tables_createtable_statement[i]
         
        st.session_state['custom_table_info'] = custom_table_info


def update_db_params():
    if st.session_state['selected_tables']:
        st.session_state['include_tables'] = st.session_state['selected_tables']
        st.session_state['sample_rows_in_table_info'] = st.session_state['sample_rows']
        st.session_state['sql_db'] = SQLDatabase.from_uri("sqlite:///" + st.session_state['db_path'],
                                                          include_tables=st.session_state['include_tables'],
                                                          sample_rows_in_table_info=st.session_state['sample_rows_in_table_info']
                                                          )
        
        st.session_state['sql_toolkit'] = SQLDatabaseToolkit(db=st.session_state['sql_db'],
                                                            llm=st.session_state['llm']
                                                            )
        
        tables_createtable_statement = st.session_state['sql_db'].get_table_info().split("CREATE TABLE")[1:]
        custom_table_info = {}

        for i in range(len(tables_createtable_statement)):
            custom_table_info[st.session_state['include_tables'][i]] = "CREATE TABLE " + tables_createtable_statement[i]
        
        st.session_state['custom_table_info'] = custom_table_info
        st.toast(f"Updated DB Params", icon="✅")

def update_table_info(table_id):

        edited_info_dict = {}  

        for i, table_name in enumerate(st.session_state['include_tables']):
            edited_info = st.session_state.get(f'table_info_editor_{i}', None)
            if edited_info:
                edited_info_dict[table_name] = edited_info

        for key in edited_info_dict.keys():
            st.session_state['custom_table_info'][key] = edited_info_dict[key]
        
        st.session_state['sql_db'] = SQLDatabase.from_uri("sqlite:///" + st.session_state['db_path'],
                                                          include_tables=st.session_state['include_tables'], 
                                                          sample_rows_in_table_info=st.session_state['sample_rows_in_table_info'],
                                                          custom_table_info=st.session_state['custom_table_info'])
        
        st.session_state['sql_toolkit'] = SQLDatabaseToolkit(db=st.session_state['sql_db'],
                                                             llm=st.session_state['llm']
                                                             )
        st.toast(f"Updated **{st.session_state['include_tables'][table_id]}** table info", icon='✅')


if st.session_state['openai_api_key'] != '':

    st.subheader('Edit Database Information')

    c1, c2 = st.columns([4,1], gap='large')
    with c1:
        selected_tables = st.multiselect("Include Tables:",
                                        options=st.session_state['table_names'],
                                        default=st.session_state['include_tables'],
                                        on_change=update_db_params,
                                        key='selected_tables'
                                        )
    with c2:
        sample_rows = st.slider('Number of Sample Rows:',
                                min_value=0,
                                max_value=10,
                                value=2,
                                on_change=update_db_params,
                                key='sample_rows'
                                )


    if st.session_state['selected_tables']:
        tabs = st.tabs(st.session_state['include_tables'])
        i = 0
        for tab in tabs:
            with tab:
                st.text_area("`Table info`",
                            st.session_state['custom_table_info'][st.session_state['include_tables'][i]],
                            height=500,
                            on_change=update_table_info,
                            key=f'table_info_editor_{i}',
                            args=[i],
                            label_visibility='collapsed')
                i += 1
        with st.expander("All tables info"):
            st.text(st.session_state['sql_toolkit'].get_tools()[0].db.table_info)
    else:
        st.warning("Select at least one table")
else:
    st.error('Please load OpenAI API KEY', icon='🚨')