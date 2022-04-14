from re import template
import pandas as pd
import json
import time
import uvicorn
import os
import shutil
from fastapi import FastAPI, Request
from random import sample
from transformers import pipeline
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
import os
from transformers import AutoConfig


# def parse_dataframe(df):
#     result = df.to_json(orient="records")
#     parsed=json.loads(result)
#     return parsed


app = FastAPI(
    title = "NEW API",
    description = "API helps analyze news articles"
)

#app.mount("/static", StaticFiles(directory="static"), name="static")
print("DEBUGG")
print(os.getcwd())
print(os.listdir())

model = "t5-small"
model_path = os.path.join(os.getcwd(), model) 
if not os.path.exists(model_path):
    os.makedirs(model_path)
    if os.path.exists("config.json"):
            shutil.move("config.json", model_path)
    print("DEBUGG -- 2")
    print(os.listdir(model_path))

# summarizer = pipeline("summarization", model=model, tokenizer=model)
config = AutoConfig.from_pretrained('t5-small')

summarizer = pipeline("summarization")


#nlp = spacy.load("en_core_web_sm")

file = pd.read_csv("./eventnarratives.csv")
#print(file.head())
#file.head()

# API
@app.get("/")
def read_root():     
    return {"message": "Welcome from the Weather Application"}


#NER
# row = file.sample()
# episode_narrative = row['EPISODE_NARRATIVE'].values
# event_narrative = str(row['EVENT_NARRATIVE'])

# def ner_spacy(text):
#     doc1 = nlp(text)
#     for ent in doc1.ents:
#         yield ent.text, ent.label_


# @app.post("/ner")
# def ner():
#     row = file.sample()
#     episode_narrative = row['EPISODE_NARRATIVE'].values
#     #event_narrative = str(row['EVENT_NARRATIVE'])
#     episode_str = str(episode_narrative)

#     doc = nlp(episode_str)
#     ents=[]
#     #ner1 = displacy.render(doc, style='ent', jupyter=True)
#     for ent in doc.ents:
#             ents.append({"text": ent.text, "label": ent.label_})

#     return {"ents": ents}

# templates = Jinja2Templates(directory='app')

# @app.post("/display_ner", response_class=HTMLResponse)
# def display_ner():
#     row = file.sample()
#     episode_narrative = row['EPISODE_NARRATIVE'].values
#     episode_str = str(episode_narrative)

#     doc1 = nlp(episode_str)
#     return templates.TemplateResponse("item.html")


# episode_str = str(episode_narrative)

# print(event_narrative)
# A weak low pressure area brought a period of sleet and freezing rain to southern WI. Up to one half inch of sleet accumulation and a tenth of an inch of ice accumulation occurred. Some vehicle slide-offs and accidents occurred.  There were a small number of power outages mostly in far southeast WI.
# txt = "An area of low pressure over southern Manitoba the morning of the 15th moved to near southern Hudson Bay by the morning of the 16th. A cold front associated with this low moved across the Northland during the afternoon and evening hours of the 15th. A warm front had moved through on the previous day brought a warm and unstable airmass in its wake. The cold front then worked with this airmass to create severe storms from northeast Minnesota into northwest Wisconsin and western Lake Superior. Damaging winds accounted for most of the reports with these storms, although there was some marginally severe hail as well. Most of the damage was to trees, but some property damage to pontoon boats and a home also occurred."

# nlp = spacy.load("en_core_web_sm")

# doc = nlp(episode_str)

# displacy.render(doc, style='ent', jupyter=True)

#SUMMARIZE
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
#summarizer = pipeline(task="summarization", model="sshleifer/distilbart-cnn-6-6", tokenizer="sshleifer/distilbart-cnn-6-6",framework="pt")

# summarizer2 = pipeline("summarization",model="t5-small", tokenizer="t5-small")

# def summarize(text):
#     summary = summarizer2(text, max_length=40, min_length=20, do_sample=False)
#     return summary

# summarize(episode_str)

@app.post("/{row_id}/summarizer")
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
