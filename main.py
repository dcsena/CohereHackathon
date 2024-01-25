import os
from io import StringIO
from time import time
import cohere
import numpy as np
import pandas as pd
import streamlit as st
import json

from Recommender import Recommender

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
COHERE_MODEL_NAME = os.environ["CO_MODEL_NAME"]
co = cohere.Client(COHERE_API_KEY)
recommender = Recommender(co, COHERE_MODEL_NAME)

DATASET_PATH = "./output/job_descriptions.json"

RESULTS_LIMIT = 3


def get_embeddings():
    with open(DATASET_PATH, 'r', encoding='utf-8') as file:
        job_descriptions = json.load(file)
        jd_df = pd.DataFrame(job_descriptions)
        embeds = co.embed(texts=list(jd_df),
                          model=COHERE_MODEL_NAME).embeddings
    return jd_df, embeds


st.set_page_config(layout="wide")
st.markdown("## Let's find the best job for you.")


@st.cache_data()
def setup():
    jd_df, embeddings = get_embeddings()
    candidates = np.array(embeddings, dtype=np.float32)
    return jd_df, candidates


jd_df, candidates = setup()

job_postings = sorted(jd_df.jobId.tolist())
print(job_postings)
images_cache = {}

uploaded_file = st.file_uploader("Upload your resume", type="txt")
input_resume = None
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    input_resume = stringio.read()
    st.write(input_resume)

retrieve_button = st.button("fetch!")
if input_resume or retrieve_button:
    print(f"Querying resume")
    start_time = time()
    result = recommender.get_similarity(input_resume, candidates=candidates, top_k=RESULTS_LIMIT)
    print(result)
    end_time = time()

    similar_results = {}
    for index, hit in enumerate(result):
        print(hit)
        similar_example = jd_df.iloc[index]
        similar_results[index] = similar_example

    print("Similar Results:")
    print(similar_results)
    for index in range(0, len(similar_results), RESULTS_LIMIT):
        cols = st.columns(RESULTS_LIMIT)
        for i in range(RESULTS_LIMIT):
            try:
                cols[i].markdown(f"**jobId**: {similar_results[index + i]['jobId']}")
                cols[i].markdown(f"**Role**: {similar_results[index + i]['role']}")
                cols[i].markdown(f"**Department**: {similar_results[index + i]['department']}")
            except:
                continue

    st.markdown(f"search latency = {end_time - start_time:.4f}s")
