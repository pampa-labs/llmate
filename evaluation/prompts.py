from langchain.prompts import PromptTemplate

template = """You are a judge grading a model's answer.
You are given a question, the model's answer, and the true answer and you need to determine whether the answer is 'Correct' or 'Incorrect'.
 
When grading, ignore any differences in punctuation and just consider the factual accuracy. Begin!

QUESTION: {query}
MODEL ANSWER: {result}
TRUE ANSWER: {answer}
GRADE:"""

GRADING_PROMPT = PromptTemplate(input_variables=["query", "result", "answer"], template=template)

target_template = """
Given an input question, a query and its result construct an answer to the original question

Question: {question}
SQLQuery: {query}
SQLResult: {query_result}
Answer:
"""

TARGET_PROMPT = PromptTemplate(input_variables=["question", "query", "query_result"], template=target_template)