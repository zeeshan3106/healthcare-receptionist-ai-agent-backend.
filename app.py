from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.tools import tool
import requests 
import sqlite3
from fastapi import FastAPI,Body
from fastapi.responses import JSONResponse
from mthcemail import EmailSend
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
embedding = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



class State(TypedDict):
    query:str
    dept:Literal['eyecare','dental','speech','mental','pysio']
    res:str
    name:str
    contact:str
    email:str
    dept:str
    service:str
    specialist:str
    desc:str
    appointment_fee:int

class Dept(TypedDict):
    dept:Literal['eyecare','dental','speech','mental','pysio']



@tool
def EyecareTool(
    name:str,
    contact:str,
    email:str,
    dept:str,
    service:str,
    specialist:str,
    desc:str,
    appointment_fee:int,
    time:str,
    State:State):
    """
    Tool
    """
    payload = {
        'name':name,
        'contact':contact,
        'email':email,
        'dept':dept,
        'service':service,
        'specialist':specialist,
        'desc':desc,
        'appointment_fee':appointment_fee,
        'time':time
        }
    API = ""
    res = requests.post(API,payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with EyeCare Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final


@tool
def DentalTool(
    name:str,
    contact:str,
    email:str,
    time:str,
    dept:str,
    service:str,
    specialist:str,
    desc:str,
    appointment_fee:int,
    State:State):
    """
    Tool
    """
    payload = {
        'name':name,
        'contact':contact,
        'email':email,
        'dept':dept,
        'service':service,
        'specialist':specialist,
        'desc':desc,
        'appointment_fee':appointment_fee
        }
    API = ""
    res = requests.post(API,payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with MTHC Dental Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final


@tool
def SpeechTool(
    name:str,
    contact:str,
    time:str,
    email:str,
    dept:str,
    service:str,
    specialist:str,
    desc:str,
    appointment_fee:int,
    State:State):
    """
    Tool
    """
    payload = {
        'name':name,
        'contact':contact,
        'email':email,
        'dept':dept,
        'service':service,
        'specialist':specialist,
        'desc':desc,
        'appointment_fee':appointment_fee
        }
    API = ""
    res = requests.post(API,payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with MTHC Speech Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final
  
    
@tool
def MentalTool(
    name:str,
    contact:str,
    time:str,
    email:str,
    dept:str,
    service:str,
    specialist:str,
    desc:str,
    appointment_fee:int,
    State:State):
    """
    Tool
    """
    payload = {
        'name':name,
        'contact':contact,
        'email':email,
        'dept':dept,
        'service':service,
        'specialist':specialist,
        'desc':desc,
        'appointment_fee':appointment_fee
        }
    API = ""
    res = requests.post(API,payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with MTHC Mental Health Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final

@tool
def PhysioTool(
    name:str,
    contact:str,
    time:str,
    email:str,
    dept:str,
    service:str,
    specialist:str,
    desc:str,
    appointment_fee:int,
    State:State):
    """
    Tool
    """
    payload = {
        'name':name,
        'contact':contact,
        'email':email,
        'dept':dept,
        'service':service,
        'specialist':specialist,
        'desc':desc,
        'appointment_fee':appointment_fee
        }
    API = ""
    res = requests.post(API,payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with MTHC Physio Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final




def Analyze(State:State):
    query = State['query']
    prompt = f"this is the {query} from user categorise it like from which department user is talking about if not provided simply ask that "
    smodel = model.with_structured_output(Dept)
    result = smodel.invoke(prompt)
    State['dept']=result['dept']

    return {
        'dept':State['dept']
    }

def Eyecare(State:State):
    query = State['query']
    API = "mongodb://zeeshanalizafar53_db_user:K0Ae9OB2vKrhJOhP@ac-xw9edx7-shard-00-00.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-01.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-02.laivntp.mongodb.net:27017/?ssl=true&replicaSet=atlas-j0742x-shard-0&authSource=admin&appName=AI-Database"
    collection = State['dept']
    client = MongoClient(API)
    database = client['MTHC']
    collection = database[collection]
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs = {
            'k':10
        }

    )
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from user ans from our rag db{retrieved} only run otherwise not Eyecaretool when all credentials for booking are avaiable only"
    smodel = model.bind_tools([EyecareTool])
    result = smodel.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final

    return {
        'res':State['res']
    }


def Dental(State:State):
    query = State['query']
    API = "mongodb://zeeshanalizafar53_db_user:K0Ae9OB2vKrhJOhP@ac-xw9edx7-shard-00-00.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-01.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-02.laivntp.mongodb.net:27017/?ssl=true&replicaSet=atlas-j0742x-shard-0&authSource=admin&appName=AI-Database"
    collection = State['dept']
    client = MongoClient(API)
    database = client['MTHC']
    collection = database[collection]
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs = {
            'k':10
        }

    )
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from user ans  from our rag db ,only run otherwise not DentalTool when all credentials for booking are avaiable only"
    smodel = model.bind_tools([DentalTool])
    result = smodel.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final

    return {
        'res':State['res']
    }

def Speech(State:State):
    query = State['query']
    API = "mongodb://zeeshanalizafar53_db_user:K0Ae9OB2vKrhJOhP@ac-xw9edx7-shard-00-00.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-01.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-02.laivntp.mongodb.net:27017/?ssl=true&replicaSet=atlas-j0742x-shard-0&authSource=admin&appName=AI-Database"
    collection = State['dept']
    client = MongoClient(API)
    database = client['MTHC']
    collection = database[collection]
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs = {
            'k':10
        }

    )
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from user ans from our rag db{retrieved} ,only run otherwise not SpeechTool when all credentials for booking are avaiable only"
    smodel = model.bind_tools([SpeechTool])
    result = smodel.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final

    return {
        'res':State['res']
    }



def Mental(State:State):
    query = State['query']
    API = "mongodb://zeeshanalizafar53_db_user:K0Ae9OB2vKrhJOhP@ac-xw9edx7-shard-00-00.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-01.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-02.laivntp.mongodb.net:27017/?ssl=true&replicaSet=atlas-j0742x-shard-0&authSource=admin&appName=AI-Database"
    collection = State['dept']
    client = MongoClient(API)
    database = client['MTHC']
    collection = database[collection]
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs = {
            'k':10
        }

    )
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from user ans from our rag db{retrieved} ,only run otherwise not MentalTool ntal when all credentials for booking are avaiable only"
    smodel = model.bind_tools([MentalTool])
    result = smodel.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final

    return {
        'res':State['res']
    }

def Physio(State:State):
    query = State['query']
    API = "mongodb://zeeshanalizafar53_db_user:K0Ae9OB2vKrhJOhP@ac-xw9edx7-shard-00-00.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-01.laivntp.mongodb.net:27017,ac-xw9edx7-shard-00-02.laivntp.mongodb.net:27017/?ssl=true&replicaSet=atlas-j0742x-shard-0&authSource=admin&appName=AI-Database"
    collection = State['dept']
    client = MongoClient(API)
    database = client['MTHC']
    collection = database[collection]
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs = {
            'k':10
        }

    )
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from   user ans from our rag db{retrieved} ,only run otherwise not PhysioTool when all credentials for booking are avaiable only"
    smodel = model.bind_tools([PhysioTool])
    result = smodel.invoke(prompt)
    final = result.content[0]['text']
    State['res']=final

    return {
        'res':State['res']
    }


def condition(State:State):
    dept = State['dept']
    
    if dept == "eyecare":
        return "eyecare"
    if dept == "dental":
        return "dental"
    if dept == "speech":
        return "speech"
    if dept == "mental":
        return "mental"
    if dept == "pysio":
        return "pysio"
    if dept == "":
        return "analyze"


graph = StateGraph(State)
graph.add_node('analyze', Analyze)
graph.add_node('eyecare', Eyecare)
graph.add_node('dental', Dental)
graph.add_node('speech', Speech)
graph.add_node('mental', Mental)
graph.add_node('pysio', Physio)


graph.add_edge(START, 'analyze')
graph.add_conditional_edges('analyze', condition)
graph.add_edge('eyecare',END)
graph.add_edge('dental',END)
graph.add_edge('speech',END)
graph.add_edge('mental',END)
graph.add_edge('pysio',END)

connect = sqlite3.connect(database = "ABC.db", check_same_thread=False)
checkpointer = SqliteSaver(connect)
config = {'configurable':{'thread_id':1}}
workflow = graph.compile(checkpointer = checkpointer)


@app.post('/Agent')
def Query(query:str = Body(...)):
    initial_state={'query':query}
    final = workflow.invoke(initial_state, config=config)
    return JSONResponse(status_code = 200, content = final)



