import json

import pandas as pd
import streamlit as st

import llmate_config
from evaluation.evaluation import run_evaluation

llmate_config.general_config()

if ("openai_api_key" not in st.session_state) or (
    st.session_state["openai_api_key"] == ""
):
    st.error("Please load OpenAI API KEY and connect to a database", icon="🚨")
else:
    # Keep dataframe in memory to accumulate experimental results
    if "summary_df" not in st.session_state:
        summary = pd.DataFrame(columns=["Answer Grade", "Avg Latency", "Avg Tokens"])
        st.session_state.summary_df = summary
        print(summary)
    else:
        summary = st.session_state.summary_df

    if "evaluation_set" not in st.session_state:
        with open(st.session_state['database_options'][st.session_state['database_selection']]['evaluation'], "r") as file:
            st.session_state["evaluation_set"] = json.load(file)

    if "eval_set_name" not in st.session_state:
        st.session_state["eval_set_name"] = "Chinook"
    # App
    # st.header("`LLMate`")
    st.subheader("Evaluate your Solution")
    st.markdown(
        """
    If you are loading your own JSON to use as an evaluation dataset, make sure it has the **same format** as the preloaded one:
    - **'question'**: the user's question
    - **'sql_query'**: target query that the agent should generate to get the answer to the question 
    """
    )

    st.markdown(
        """
    Here you can take a look at the evaluation set, as well as edit what has been uploaded or add new queries to be evaluated:
    """
    )

    edited_data = st.data_editor(
        st.session_state["evaluation_set"], num_rows="dynamic", key="eval_set_editor"
    )

    if st.button("Evaluate Agent"):
        # eval_set = st.session_state['evaluation_set']
        eval_set = edited_data
        db = st.session_state["sql_db"]
        sql_agent = st.session_state["sql_agent"]

        # Grade model
        (
            graded_answers,
            latency,
            predictions,
            targets,
            answer_toks,
            target_toks,
            grade_toks,
        ) = run_evaluation(sql_agent, eval_set, db)

        # Assemble outputs
        d = pd.DataFrame(predictions)
        d["expected_answer"] = targets
        d["answer score"] = [g["results"] for g in graded_answers]
        d["latency"] = latency
        d["tokens"] = answer_toks
        d["graded_answers"] = graded_answers

        st.session_state["eval_data"] = d

        st.info(
            f"""Evaluation completed. Evaluation costs were as follows:

        * {sum(answer_toks)} tokens getting the answers for each question (gpt-turbo-3.5)

        * {sum(target_toks)} tokens dynamically computing the targets for each question (text-davinci-003)
    
        * {grade_toks} grading the solution (gpt-turbo-3.5)`

        In total, {sum(target_toks) + sum(answer_toks) + grade_toks} tokens were used.
    
        """
        )

        # Summary statistics
        mean_latency = d["latency"].mean()
        mean_tokens = d["tokens"].mean()
        correct_answer_count = len(
            [text for text in d["answer score"] if "Incorrect" not in text]
        )
        percentage_answer = (correct_answer_count / len(d["graded_answers"])) * 100

        st.subheader("All Experiments")
        new_row = pd.DataFrame(
            {
                "model": [st.session_state["openai_model"]],
                "Answer Grade": [percentage_answer],
                "Avg Latency": [mean_latency],
                "Avg Tokens": [mean_tokens],
            }
        )
        st.session_state.summary_df = pd.concat([summary, new_row], ignore_index=True)
        st.session_state.summary_df.index.name = "Exp Number"

    if "eval_data" in st.session_state:
        st.header("Results")

        st.subheader("Last Run")

        st.dataframe(
            data=st.session_state["eval_data"],
            use_container_width=True,
            hide_index=True,
        )

        st.dataframe(data=st.session_state["summary_df"], use_container_width=True)
