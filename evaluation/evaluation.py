import time
from typing import List

import pandas as pd
import streamlit as st
from langchain import LLMChain, OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.evaluation.qa import QAEvalChain

from evaluation.prompts import GRADING_PROMPT, TARGET_PROMPT

if "summary_df" not in st.session_state:
    summary = pd.DataFrame(columns=['model',
                                    'Latency',
                                    'Answer Grade'])
    st.session_state.summary_df = summary
else:
    summary = st.session_state.summary_df

def grade_answer(eval_dataset: List, predictions: List) -> List:

    with st.spinner(text="Grading answers..."):

        eval_chain = QAEvalChain.from_llm(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
            prompt=GRADING_PROMPT
        )

        with get_openai_callback() as cb:
            graded_outputs = eval_chain.evaluate(
                eval_dataset,
                predictions,
                question_key="question",
                prediction_key="result"
            )

    return graded_outputs, cb.total_tokens

def get_target(question, query, db):

    q_result = db.run(query)

    llm = OpenAI(temperature=0)
    llm_chain = LLMChain(
        llm=llm,
        prompt=TARGET_PROMPT
    )

    with get_openai_callback() as cb:
        res = llm_chain.run({'question': question, 'query': query, 'query_result': q_result})

    return res, cb.total_tokens


def run_evaluation(agent, eval_set, db):

    st.info("`Running agent on all examples...`")
    predictions = []
    eval_dataset = []
    latencies = []
    answer_toks_ls = []
    target_toks_ls = []

    progress_bar = st.progress(0)

    for e,data in enumerate(eval_set):
        
        progress_bar.progress((e + 1) / len(eval_set))

        start_time = time.time()

        with get_openai_callback() as cb:
            answer = agent.run(data["question"])
            answer_toks = cb.total_tokens

        target, target_toks = get_target(data["question"], data["sql_query"], db)

        predictions.append({"question": data["question"], "answer": target, "result": answer})
        eval_dataset.append(data)
        end_time = time.time()
        elapsed_time = end_time - start_time
        latencies.append(elapsed_time)
        answer_toks_ls.append(answer_toks)
        target_toks_ls.append(target_toks)

    answers_grade, grade_toks_ls = grade_answer(eval_dataset, predictions)
    return answers_grade, latencies, predictions, answer_toks_ls, target_toks_ls, grade_toks_ls