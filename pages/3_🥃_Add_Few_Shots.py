import json

import llmate_config
import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.agent_types import AgentType
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS

llmate_config.general_config()
llmate_config.init_session_state()


def update_agent():
    few_shots = st.session_state["few_shots"]

    embeddings = OpenAIEmbeddings()

    few_shot_docs = [
        Document(
            page_content=example["question"],
            metadata={"sql_query": example["sql_query"]},
        )
        for example in few_shots
    ]
    vector_db = FAISS.from_documents(few_shot_docs, embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    description = """
    This tool will help you understand similar examples to adapt them to the user question.
    Input to this tool should be the user question.
    """

    retriever_tool = create_retriever_tool(
        retriever, name="sql_get_similar_examples", description=description
    )

    st.session_state[
        "sql_agent_suffix"
    ] = "Always use the 'sql_get_similar_examples' tool before using any other tool."

    st.session_state["sql_agent"] = create_sql_agent(
        llm=st.session_state["llm"],
        toolkit=st.session_state["sql_toolkit"],
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        prefix=st.session_state["sql_agent_prefix"],
        suffix=st.session_state["sql_agent_suffix"],
        extra_tools=[retriever_tool],
    )
    st.toast("Agent saved 🔥")


if (st.session_state["openai_api_key"] != "") & (st.session_state["db_uri"] != ""):
    st.subheader("Add few shot examples")
    st.markdown(
        """
    If your agent is having trouble answering some complex questions, giving it some concrete examples might work.
    
    In fact, adding few shot examples to your prompt has been [proven](https://arxiv.org/abs/2204.00498) to improve accuracy significantly when dealing with hard questions.

    If you want to include few shot examples in your prompt, make sure it has the **following format**:
    - **'question'**: the user's question
    - **'sql_query'**: target query that the agent should generate to get the answer to the question 
    """
    )

    uploaded_few_shots = st.file_uploader(
        "Please upload a few shot dataset (.json): ",
        type=["json"],
        accept_multiple_files=False,
    )

    if uploaded_few_shots:
        st.session_state["few_shots"] = json.loads(uploaded_few_shots.read())
        st.session_state["few_shots.name"] = uploaded_few_shots.name 

        st.markdown(
            """
        Take a look at the few shot examples you would be adding, and edit them at will
        """
        )

        edited_data = st.data_editor(
            st.session_state["few_shots"],
            num_rows="dynamic",
            key="few_shots_editor",
            use_container_width=True,
            on_change=update_agent,
        )


else:
    st.error("Please load OpenAI API KEY and a database", icon="🚨")
