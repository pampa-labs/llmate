import streamlit as st
from langchain.agents.agent_toolkits.sql.prompt import SQL_PREFIX


import llmate_config
llmate_config.general_config()

if st.session_state['openai_api_key'] != '':

    st.info("To recreate this Agent in your solution, copy and paste the code below:")


    #TODO Meter bien el model
    #TODO agregar imports
    #TODO Custom table info es siempre un choclazo

    # First we define the logic to see wether we need to specify params or not:
    changing_tables = (st.session_state['include_tables'] != st.session_state['table_names'])
    changing_prefix = (st.session_state['sql_agent_prefix'] != SQL_PREFIX)

    code = f'''
    from langchain.llms import OpenAI
    from langchain.utilities import SQLDatabase
    from langchain.agents.agent_toolkits import SQLDatabaseToolkit
    from langchain.agents.agent_types import AgentType
    from langchain.agents import create_sql_agent


    llm = OpenAI(temperature=0, verbose=True)

    '''

    if changing_tables:
        code += f"# List containing the tables to include \ninclude_tables = {st.session_state['include_tables']}\n\n"

    if 'custom_table_info' in st.session_state:
        code += f'# Custom table info \ncustom_table_info = {st.session_state["custom_table_info"]}\n\n'

    code += '# Replace with your database URI\ndatabase_uri = "sqlite:///your-database-uri"\n\n# Load DB\nsql_db = SQLDatabase.from_uri(database_uri,'

    if changing_tables:
        code += '''
        include_tables=include_tables,'''


    code += f'''
        sample_rows_in_table_info={st.session_state['sample_rows_in_table_info']},
        custom_table_info=custom_table_info
    )


    sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)
    '''

    if changing_prefix:
        code += f'''
        agent_prefix = """
        {st.session_state['sql_agent_prefix']}
        """
        '''

    code += '''
    agent = create_sql_agent(
        llm = llm,
        toolkit=sql_toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    '''
    if changing_prefix:
        code += 'prefix=agent_prefix'

    code +=''')
        '''
    st.code(code, language='python')
else:
    st.error('Please load OpenAI API KEY', icon='🚨')