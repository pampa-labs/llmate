import streamlit as st
from langchain.utilities import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType


import llmate_config
llmate_config.general_config()
llmate_config.init_session_state()

if ('openai_api_key' not in st.session_state) or (st.session_state['openai_api_key'] == ''):
    st.error('Please load OpenAI API KEY and connect to a database', icon='🚨')
else:
    if 'custom_table_info' not in st.session_state:
            tables_createtable_statement = st.session_state['sql_db'].get_table_info().split("CREATE TABLE")[1:]
            custom_table_info = {}

            for i in range(len(tables_createtable_statement)):
                custom_table_info[st.session_state['table_names'][i]] = "CREATE TABLE " + tables_createtable_statement[i]
            st.session_state['custom_table_info'] = custom_table_info

    def update_db_params():
        if st.session_state['selected_tables']:
            st.session_state['include_tables'] = st.session_state['selected_tables']
            # st.session_state['sample_rows_in_table_info'] = st.session_state['sample_rows']
            st.session_state['sql_db'] = SQLDatabase.from_uri(st.session_state['db_uri'],
                                                            include_tables=st.session_state['include_tables'],
                                                            sample_rows_in_table_info=st.session_state['sample_rows_in_table_info']
                                                            )
            
            st.session_state['sql_toolkit'] = SQLDatabaseToolkit(db=st.session_state['sql_db'],
                                                                llm=st.session_state['llm'],
                                                                custom_table_info=st.session_state['custom_table_info']
                                                                )
            st.session_state['sql_agent'] = create_sql_agent(
                llm = st.session_state['llm'],
                toolkit=st.session_state['sql_toolkit'],
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                prefix=st.session_state['sql_agent_prefix'],
                suffix=st.session_state['sql_agent_suffix']
            )
            
            tables_createtable_statement = st.session_state['sql_db'].get_table_info().split("CREATE TABLE")[1:]
            custom_table_info = {}

            for i in range(len(tables_createtable_statement)):
                custom_table_info[st.session_state['include_tables'][i]] = "CREATE TABLE " + tables_createtable_statement[i]
            
            st.session_state['custom_table_info'] = custom_table_info

    def update_table_info(table_id=None):

        edited_info_dict = {}  

        for i, table_name in enumerate(st.session_state['include_tables']):
            edited_info = st.session_state.get(f'table_info_editor_{i}', None)
            if edited_info:
                edited_info_dict[table_name] = edited_info

        for key in edited_info_dict.keys():
            st.session_state['custom_table_info'][key] = edited_info_dict[key]
            print("Edited key", key)
            print(st.session_state['custom_table_info'][key])
        
        st.session_state['sql_db'] = SQLDatabase.from_uri(st.session_state['db_uri'],
                                                            include_tables=st.session_state['include_tables'], 
                                                            sample_rows_in_table_info=st.session_state['sample_rows_in_table_info'],
                                                            custom_table_info=st.session_state['custom_table_info'])
        
        st.session_state['sql_toolkit'] = SQLDatabaseToolkit(db=st.session_state['sql_db'],
                                                                llm=st.session_state['llm']
                                                                )
        st.session_state['sql_agent'] = create_sql_agent(
            llm = st.session_state['llm'],
            toolkit=st.session_state['sql_toolkit'],
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            prefix=st.session_state['sql_agent_prefix'],
            suffix=st.session_state['sql_agent_suffix']
        )

        # update_db_params()
        if table_id is not None:
            st.toast(f"Updated **{st.session_state['include_tables'][table_id]}** table info", icon='✅')


    st.subheader('Edit Database Information')
    st.markdown(
    """
    The Agent receives the DDL statements and some example rows for each table. 
    Here you can choose which tables to include, how many rows to show and edit the table information to be used later in the prompt. 
    """
    )

    # c1, c2 = st.columns([4,1], gap='large')
    # with c1:
    selected_tables = st.multiselect("Select tables to be included:",
                                        options=st.session_state['table_names'],
                                        default=st.session_state['include_tables'],
                                        on_change=update_db_params,
                                        key='selected_tables'
                                        )
    # with c2:
    #     sample_rows = st.slider('Number of Sample Rows:',
    #                             min_value=0,
    #                             max_value=10,
    #                             value=2,
    #                             on_change=update_db_params,
    #                             key='sample_rows'
    #                             )
    # update_db_params()


    if st.session_state['selected_tables']:
        tabs = st.tabs(st.session_state['include_tables'])
        i = 0
        for tab in tabs:
            with tab:
                st.text_area("`Table info`",
                            value=st.session_state['custom_table_info'][st.session_state['include_tables'][i]],
                            height=500,
                            on_change=update_table_info,
                            key=f'table_info_editor_{i}',
                            args=[i],
                            label_visibility='collapsed')
                i += 1
        with st.expander("View table info to be received by the Agent"):
            st.text(st.session_state['sql_toolkit'].get_tools()[0].db.table_info)
    else:
        st.warning("Select at least one table")
