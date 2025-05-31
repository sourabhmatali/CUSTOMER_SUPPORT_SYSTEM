import uvicorn #for fastapi
from fastapi import FastAPI, Request, Form #for fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough #here importing  RunnablePassthrough from langchain/to give question at a runtime

from langchain_core.output_parsers import StrOutputParser #here importing  StrOutputParser from langchain

from langchain_core.prompts import ChatPromptTemplate #here importing  chatprompttemplate from langchain

from retriever.retrieval import Retriever #here from retriever folder-->retrieval file --->importing class Retriever

from utils.model_loader import ModelLoader #here from utils folder--->model_loader file ---->importing class Modelloader

from prompt_library.prompt import PROMPT_TEMPLATES #here from prompt_library folder ---> prompt file ---> importing  PROMPT_TEMPLATES


app = FastAPI() #initializing the fast api
app.mount("/static", StaticFiles(directory="static"), name="static") #here we are inserting .css file /we are mounting 
templates = Jinja2Templates(directory="templates") #here defining the jinja template
# Allow CORS (optional for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

retriever_obj = Retriever() #here creating object of the retriever

model_loader = ModelLoader()#here creating object of the model loader

def invoke_chain(query:str): #here function named invoke_chain it will take query as input which is str 
    
    retriever=retriever_obj.load_retriever() #here using load_retriever() function on object of the retriever
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATES["product_bot"]) #here loading prompt from PROMPT_TEMPLATES which is defined inside prompt.py
    llm= model_loader.load_llm() #here using load_llm() function on the object of the ModelLoader
    
    chain=( #creating LCEL chain
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    
    )
    
    output=chain.invoke(query)
    
    return output

@app.get("/", response_class=HTMLResponse) #it will make request to the server
async def index(request: Request):
    """
    Render the chat interface.
    """
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/get",response_class=HTMLResponse) #submitting something to server and getting back the response
async def chat(msg:str=Form(...)): #here creating async method ,it will take msg of type str from form
    result=invoke_chain(msg) #here invoking
    print(f"Response: {result}") 
    return result #here returning again result