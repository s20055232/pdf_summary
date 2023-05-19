from fastapi import FastAPI, UploadFile, File, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
from typing import Annotated
from fastapi.responses import JSONResponse
from pathlib import Path

from llama_index import GPTVectorStoreIndex, download_loader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


load_dotenv(find_dotenv())

past_loader = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

options = []


class Item(BaseModel):
    file_name: str
    query: str


@app.get("/")
def read_root():
    return {"Hello": "world"}


@app.post("/upload/")
def upload_pdf_file(file: Annotated[UploadFile, File()]):
    with open(f"./resource/{file.filename}", "wb+") as f:
        f.write(file.file.read())

    global options
    options.append(file.filename)
    return "Save Complete"


@app.post("/parsing")
def answer_query(item: Annotated[Item, Body()]):
    CJKPDFReader = download_loader("CJKPDFReader")
    loader = CJKPDFReader()
    documents = loader.load_data(file=Path(f"./resource/{item.file_name}"))
    global past_loader
    if item.file_name in past_loader:
        index = past_loader[item.file_name]
    else:
        index = GPTVectorStoreIndex.from_documents(documents)
        past_loader[item.file_name] = loader

    try:
        response = index.query(item.query)
        return response
    except:
        return {"messgage": "Some error happened"}


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
