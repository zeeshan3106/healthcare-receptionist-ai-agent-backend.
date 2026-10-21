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
from fastapi.responses import JSONResponse, StreamingResponse
from mthcemail import EmailSend
from fastapi.middleware.cors import CORSMiddleware
from langgraph.config import get_stream_writer
import os
import time
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
embedding = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")
app = FastAPI()
API = os.getenv("API")
API = os.getenv("API") 

client = MongoClient(API)
database = client['MTHC']
vector_stores = {
    dept: MongoDBAtlasVectorSearch(
        embedding=embedding,
        collection=database[dept],
        index_name="vector_index",
    )
    for dept in ["eyecare", "dental", "speech", "mental", "pysio",'Hi']
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



class State(TypedDict):
    query:str
    dept:Literal['eyecare','dental','speech','mental','pysio','Hi']
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
    dept:Literal['eyecare','dental','speech','mental','pysio','Hi']



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
    writer = get_stream_writer()
    query = State['query']
    retriever = vector_stores[State["dept"]].as_retriever(
    search_kwargs={"k": 10}
)
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from user ans from our rag db{retrieved}  You are eye care Assistant just guide the individual regarding questions they ask ,  only run otherwise not Eyecaretool when all credentials for booking are avaiable only"
    smodel = model.bind_tools([EyecareTool])
    answer = []

    for chunk in smodel.stream(prompt):
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)

    return {'answer': ''.join(answer)}
    


     


def Dental(State:State):
    writer = get_stream_writer()
    query = State['query']
    retriever = vector_stores[State["dept"]].as_retriever(
    search_kwargs={"k": 10}
)
    retriever = db.as_retriever(
        search_kwargs = {
            'k':10
        }

    )
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from user ans  from our rag db ,only run otherwise not DentalTool when all credentials for booking are avaiable only"
    smodel = model.bind_tools([DentalTool])
    answer = []

    for chunk in smodel.stream(prompt):
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)

    return {'answer': ''.join(answer)}

def Speech(State:State):
    writer = get_stream_writer()
    query = State['query']
    retriever = vector_stores[State["dept"]].as_retriever(
    search_kwargs={"k": 10}
)
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from user ans from our rag db{retrieved} ,only run otherwise not SpeechTool when all credentials for booking are avaiable only"
    smodel = model.bind_tools([SpeechTool])
 

    answer = []

    for chunk in smodel.stream(prompt):
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)

    return {'answer': ''.join(answer)}



def Mental(State:State):
    writer = get_stream_writer()
    query = State['query']
    retriever = vector_stores[State["dept"]].as_retriever(
    search_kwargs={"k": 10}
)
   
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from user ans from our rag db{retrieved} ,only run otherwise not MentalTool ntal when all credentials for booking are avaiable only"
    smodel = model.bind_tools([MentalTool])
    answer = []

    for chunk in smodel.stream(prompt):
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)

    return {'answer': ''.join(answer)}

def Physio(State:State):
    writer = get_stream_writer()
    query = State['query']
    retriever = vector_stores[State["dept"]].as_retriever(
    search_kwargs={"k": 10}
)
    retrieved = retriever.invoke(query)

    prompt = f"This is the query{query} from   user ans from our rag db{retrieved} ,only run otherwise not PhysioTool when all credentials for booking are avaiable only"
    smodel = model.bind_tools([PhysioTool])
    answer = []

    for chunk in smodel.stream(prompt):
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)

    return {'answer': ''.join(answer)}


def Hi(State:State):
    writer = get_stream_writer()
    query = State['query']
    
   

    prompt = f"""This is the query{query} from  You are Melbourne Teaching and Health Clinics MTHC assistant greet user ask from user which dept he want Eyecare, Dental, Mental, pshyio ,speech pathiology salso ask he want to book appointment with some specialist   ,only run otherwise not PhysioTool when all
     credentials for booking are avaiable only

     - Always use green tick emoji for one time atleast in one message not too much
- Use other emojis relates to data but ocasionally not which all
- Always use green tick emoji for one time atleast in one message not too much
- Do not use Markdown.
- Do not use asterisks (*) for bold or bullet points.
- Do not use headings with Markdown formatting.

     
     
     
     """
    answer = []


    for chunk in model.stream(prompt):
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)

    return {'answer': ''.join(answer)}

def condition(State:State):
    dept = State['dept']
    if dept == "Hi":
        return "hi"
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
graph.add_node('hi', Hi)
graph.add_node('analyze', Analyze)
graph.add_node('eyecare', Eyecare)
graph.add_node('dental', Dental)
graph.add_node('speech', Speech)
graph.add_node('mental', Mental)
graph.add_node('pysio', Physio)


graph.add_edge(START, 'analyze')
graph.add_conditional_edges('analyze', condition)
graph.add_edge('hi',END)
graph.add_edge('eyecare',END)
graph.add_edge('dental',END)
graph.add_edge('speech',END)
graph.add_edge('mental',END)
graph.add_edge('pysio',END)

# connect = sqlite3.connect(database = "ABC.db", check_same_thread=False)
# checkpointer = SqliteSaver(connect)
# config = {'configurable':{'thread_id':1}}
workflow = graph.compile()


@app.post('/Agent')
def API(Query:str = Body(...)):
    config = {'configurable':{'thread_id':1}}
    initial_state ={'query':Query}
    return StreamingResponse(
        (
            chunk
            for chunk in workflow.stream(
                initial_state,
        
                stream_mode='custom'
            )

            if isinstance(chunk, str)
        ),
        media_type='text/plain'
    )
   


   





