import os
from typing import List

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

import vecs
from vecs.adapter import Adapter, TextEmbedding



DB_CONNECTION_STRING = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST', 'db')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'postgres')}"

with vecs.create_client(DB_CONNECTION_STRING) as vx:
    collection = vx.get_or_create_collection(name="clip_vectors", dimension=512, adapter=Adapter(
        [
            TextEmbedding(model='clip-ViT-B-32')
        ]
    ))



app = FastAPI()

class Sentence(BaseModel):
    text: str
    # description: str = None

class SentenceIngest(Sentence):
    id: str

class SentenceIngestRequest(BaseModel):
    sentences: List[SentenceIngest]

class SentenceRequest(Sentence):
    num: int=3

def ingest_collection(sentences:List[Sentence]):
    # embs = model.encode(sentences)

    records =  [
        (
            sentence.id, 
            sentence.text,
            {"text":sentence.text}
         )
        for sentence in sentences
    ]
    
    with vecs.create_client(DB_CONNECTION_STRING) as vx:
        collection = vx.get_or_create_collection(name="clip_vectors", dimension=512, adapter=Adapter(
        [
            TextEmbedding(model='clip-ViT-B-32')
        ]))
        collection.upsert(records)


def search_collection(sentence:Sentence, num=3)->List[Sentence]:
    with vecs.create_client(DB_CONNECTION_STRING) as vx:
        collection = vx.get_or_create_collection(name="clip_vectors", dimension=512, adapter=Adapter(
        [
            TextEmbedding(model='clip-ViT-B-32')
        ]))

        results = collection.query(
            data=sentence.text,
            limit=num,
            include_metadata=True,
        )
        print(results)
    

    return [Sentence(text=result[1]['text']) for result in results]



@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')

@app.put("/sentence")
def sentence_ingest(request:SentenceIngestRequest):
    ingest_collection(request.sentences)

@app.post("/search")
def sentence_retrieve_nearest(request:SentenceRequest):
    return search_collection(request, num=request.num)