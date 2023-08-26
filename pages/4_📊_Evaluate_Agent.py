import json

import pandas as pd
import streamlit as st

import llmate_config
from evaluation.evaluation import run_evaluation

llmate_config.general_config()
llmate_config.init_session_state()

# Keep dataframe in memory to accumulate experimental results
if "existing_df" not in st.session_state:
    summary = pd.DataFrame(columns=[
        'Answer Grade',
        'Latency',
        'Tokens'
        ])
    st.session_state.existing_df = summary
    print(summary)
else:
    summary = st.session_state.existing_df

if 'evaluation_set' not in st.session_state:
    with open('example/Chinook.json', 'r') as file:
        st.session_state['evaluation_set'] = json.load(file)

if 'eval_set_name' not in st.session_state:
    st.session_state['eval_set_name'] = "Chinook"
# App
# st.header("`LLMate`")
st.subheader("Evaluate your Solution")

uploaded_eval_set = st.file_uploader("Please upload eval set (.json): ",
                                        type=['json'],
                                        accept_multiple_files=False)

if uploaded_eval_set:
    st.session_state['evaluation_set'] = json.loads(uploaded_eval_set.read())
    st.session_state['eval_set_name'] = uploaded_eval_set.name
else:
    st.info(f"Pre-Loaded Evaluation Set: Chinook.json")


edited_data = st.data_editor(st.session_state['evaluation_set'],
                           num_rows="dynamic",
                           key='eval_set_editor')

if st.button("Evaluate Agent"):
    # eval_set = st.session_state['evaluation_set']
    eval_set = edited_data
    db = st.session_state['sql_db']
    sql_agent = st.session_state['sql_agent']

    # Grade model
    graded_answers, latency, predictions, answer_toks, target_toks, grade_toks = run_evaluation(
        sql_agent, 
        eval_set, 
        db
        )

    # Assemble outputs
    d = pd.DataFrame(predictions)
    d['answer score'] = [g['results'] for g in graded_answers]
    d['latency'] = latency
    d['tokens'] = answer_toks

    st.info(
    f"""Evaluation completed. Evaluation costs were as follows:

    * {sum(answer_toks)} tokens getting the answers for each question (gpt-turbo-3.5)

    * {sum(target_toks)} tokens dynamically computing the targets for each question (text-davinci-003)
 
    * {grade_toks} grading the solution (gpt-turbo-3.5)`

    In total, {sum(target_toks) + sum(answer_toks) + grade_toks} tokens were used.
  
    """)

    # Summary statistics
    mean_latency = d['latency'].mean()
    mean_tokens = d['tokens'].mean()
    correct_answer_count = len([text for text in d['answer score'] if "Incorrect" not in text])
    percentage_answer = (correct_answer_count / len(graded_answers)) * 100

    st.header("Results")

    st.subheader("Last Run")

    st.dataframe(data=d, use_container_width=True, hide_index=True)

    st.subheader("All Experiments")
    new_row = pd.DataFrame({
        'model': [st.session_state['openai_model']],
        'Answer Grade': [percentage_answer],
        'Latency': [mean_latency],
        'Tokens': [mean_tokens],
                            })
    summary = pd.concat([summary, new_row], ignore_index=True)
    print(summary)

    summary.index.name = 'Exp Number'   
    st.dataframe(data=summary, use_container_width=True)
    st.session_state.existing_df = summary