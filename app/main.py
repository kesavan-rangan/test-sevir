from helper import download_from_s3, extract_zip_file
from re import template
import pandas as pd
import json
import time
import uvicorn
from fastapi import FastAPI, Request
#from spacy import displacy
from random import sample
from transformers import pipeline
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
from transformers import AutoConfig, AutoModelForSeq2SeqLM
import os


S3_BUCKET = "sevir-models"
S3_PATH = "models/t5-small.zip"

MODEL_NAME = "t5-small"

MODEL_FILE_NAME = f"{MODEL_NAME}.zip"
MODEL_PATH = "/tmp/models"
file_name = os.path.join(MODEL_PATH, MODEL_FILE_NAME)
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

# Downloads file from S3
download_from_s3(S3_BUCKET, S3_PATH, file_name)

# Unzips the downloaded Zip file
extract_zip_file(file_name)

MODEL_LOCATION = os.path.join(MODEL_PATH, MODEL_NAME)

app = FastAPI(
    title = "NEW API",
    description = "API helps analyze news articles"
)

print("DEBUGGG -- 1")
print(os.listdir())
print("DEBUGGG -- 2")
print(os.listdir(MODEL_LOCATION))

# model = AutoModelForSeq2SeqLM.from_pretrained("MODEL_LOCATION")
summarizer = pipeline("summarization", model=MODEL_LOCATION)

file = pd.read_csv("./eventnarratives.csv")


@app.get("/welcome")
def read_root():     
    return {"message": "Welcome from the Weather Application"}


@app.get("/summarizer/{row_id}")
def summarizers(row_id: int):
    #start_time = time.time()

    row = file["EPISODE_NARRATIVE"][row_id]
    #episode_narrative = row['EPISODE_NARRATIVE'].values
    #event_narrative = str(row['EVENT_NARRATIVE'])

    episode_str = str(row)
    #end_time = time.time()
    summ1=summarizer(episode_str, max_length=130, min_length=30, do_sample=False)
    return {"summary":summ1}

handler = Mangum(app)
