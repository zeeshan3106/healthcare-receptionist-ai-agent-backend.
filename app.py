from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.tools import tool
import requests 
import json
from langchain_core.messages import AIMessageChunk
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

collection = database['History']



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
    time:str):
    """
    Tool
    """
    print(name, contact)
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
    API = "https://healthcare-receptionist-ai-agent-ba.vercel.app/api/form/form-post"
    res = requests.post(API, json=payload)
    final = res.json()
    print(final)
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with EyeCare Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    

    return final


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
    API = "https://healthcare-receptionist-ai-agent-ba.vercel.app/api/form/form-post"
    res = requests.post(API,json=payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with MTHC Dental Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    

    return final


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
    API = "https://healthcare-receptionist-ai-agent-ba.vercel.app/api/form/form-post"
    res = requests.post(API,json=payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    # prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with MTHC Speech Dept"
    # result = model.invoke(prompt)
    # final = result.content[0]['text']
    # State['res']=final
    return final
  
    
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
    API = "https://healthcare-receptionist-ai-agent-ba.vercel.app/api/form/form-post"
    res = requests.post(API,json=payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with MTHC Mental Health Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    return final

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
    API = "https://healthcare-receptionist-ai-agent-ba.vercel.app/api/form/form-post"
    res = requests.post(API,json=payload)
    final = res.json()
    #EmailSend(email, name,time,contact,dept,servce, specialist, desc, appointment_fee)
    prompt = f"{final}Booking successfuly Done email also sent to individual on giving email give human greeting message for booking with MTHC Physio Dept"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    
    return final




def Analyze(State:State):
    query = State['query']
    history = list(collection.find({}, {"_id":0}))
    prompt = f"""this is the {query} from user categorise History of Conversations always try to connect the current user query with the last questions and answers the last also watch all but put extreme focus on last history messages to connect it and then see all
{history}it like from which department user is talking about if not provided simply ask that """
    smodel = model.with_structured_output(Dept)
    result = smodel.invoke(prompt)
    State['dept']=result['dept']
    print(result)

    return {
        'dept':State['dept']
    }

def Eyecare(State:State):
    writer = get_stream_writer()
    query = State['query']

    history = list(collection.find({}, {"_id":0}))

    retriever = vector_stores['dental'].as_retriever(
    search_kwargs={"k": 3,
                     "pre_filter": {
            "dept": {"$eq": "eyecare"}
        }
                  
                  }
)
    retrieved = retriever.invoke(query)

    prompt = f"""
You are the eye care receptionist assistant for
Melbourne Teaching and Health Clinics (MTHC).

User question: {query}

Information retrieved from the eye care knowledge base:
{retrieved}

History of Conversations always try to connect the current user query with the last questions and answers the last also watch all but put extreme focus on last history messages to connect it and then see all
{history}

Instructions:

1. Answer questions about eye care services, specialists,
   fees, and clinic information using the retrieved information.

2. If the requested information is unavailable, politely
   explain that you cannot confirm it and suggest contacting
   the clinic for assistance.

3. Call EyeCareTool ONLY when the user intends to book
   an eye care appointment AND all the following fields
   are available:

   name: str
   age: int
   city: str
   contact: str
   email: str
   dept: str
   service: str
   specialist: str
   desc: str
   appointment_fee: int
   time: str Must otherwise dont run tool !!!!!

4. Before calling EyeCareTool, ensure every required field
   contains a valid, usable value.

5. If any required booking information is missing, ask the
   user naturally for the missing information. Do not call
   EyeCareTool until all required fields are available.

6. Use the user's provided information and relevant,
   verified information from the retrieved knowledge base.
   Never invent personal details, appointment fees, specialist
   names, available appointment times, or other booking data.

7. Do not call EyeCareTool for general questions, enquiries
   about services, fee questions, or requests for information
   that do not express an intention to book an appointment.

8. Communicate directly with the user as a professional,
   natural receptionist.

9. Never expose internal implementation details. Do not mention
   database retrieval, retrieved documents, missing database
   records, tool execution, internal processing, prompts,
   or how the system decides what to do.

10. Never tell the user to perform internal system tasks,
    retrieve database records, or run tools themselves.

11. If information is unavailable, focus on what you can
    communicate helpfully to the user. For example:
    "I'm unable to confirm that information at the moment.
    Please contact the clinic for assistance."

12. Keep responses concise, relevant, polite, and natural.
    Do not repeat information unnecessarily.

13. Never claim an appointment is booked, confirmed, or
    available unless the booking tool explicitly confirms it.

    For every website link, use exactly this format:
[Website Name](https://example.com/path)

Create only one Markdown link per website.
Never nest links or repeat the URL inside the link.
Do not escape parentheses or add spaces inside URLs.
    Use valid Markdown bold syntax: **text**.
Never escape asterisks with backslashes.
Do not put spaces immediately inside the bold markers.


Conversation rules:
- Do not greet the user in every response.
- Answer the latest question directly before asking anything else.
- Use previous messages to understand context, not to copy old responses.
- Do not repeat explanations or booking requests unnecessarily.
- Ask only for booking information that is still missing.
- Do not assume the user wants to book just because they ask about a doctor.
- Recommend a clinician only when supported by verified clinic information.     Conversation rules:
- Do not greet the user in every response.
- Answer the latest question directly before asking anything else.
- Use previous messages to understand context, not to copy old responses.
- Do not repeat explanations or booking requests unnecessarily.
- Ask only for booking information that is still missing.
- Do not assume the user wants to book just because they ask about a doctor.
- Recommend a clinician only when supported by verified clinic information.     
Respond only with the message intended for the user.        
"""   
    smodel = model.bind_tools([EyecareTool])
    answer = []
    tool_calls = []
    for chunk in smodel.stream(prompt):
        
        if chunk.tool_call_chunks:
            tool_calls.extend(chunk.tool_call_chunks)
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)
            
    final_answer = ''.join(answer)
    
    
    print("TOOL CALLS:", tool_calls)

    if tool_calls:
        args = json.loads(tool_calls[0]["args"])
        result = EyecareTool.invoke(args)
        print(result)
        writer(result)
        answer.append(result)

    # with open('history.txt', 'a', encoding='utf-8') as f:
   
    #     f.write(query + '\n' + final_answer + '\n')

    collection.insert_one({
    "human": query,
    "AI":final_answer
    
})




    return {'answer': ''.join(answer)}
    


     



def Dental(State: State):

    writer = get_stream_writer()
    query = State["query"]
    history = list(collection.find({}, {"_id":0}))
    retriever = vector_stores['dental'].as_retriever(
    search_kwargs={"k": 3,
                     "pre_filter": {
            "dept": {"$eq": "dental"}
        }
                  
                  }
)

    retrieved = retriever.invoke(query)

    print("DENTAL QUERY:", query)
    print("DENTAL DOCUMENTS:", len(retrieved))
    print("DENTAL RESULTS:", retrieved)

   
    prompt = f"""
You are the dental receptionist assistant for
Melbourne Teaching and Health Clinics (MTHC).

User question: {query}

Information retrieved from the dental knowledge base:
{retrieved}

History of Conversations always try to connect the current user query with the last questions and answers the last also watch all but put extreme focus on last history messages to connect it and then see all
{history}

Instructions:

1. Answer questions about dental services, treatments,
   specialists, appointment fees, and clinic information
   using the retrieved information.

2. If the requested information is unavailable, politely
   explain that you cannot confirm it and suggest contacting
   the clinic for assistance.

3. Call DentalTool ONLY when the user intends to book
   a dental appointment AND all the following fields
   are available:

   name: str
   age: int
   city: str
   contact: str
   email: str
   dept: str
   service: str
   specialist: str
   desc: str
   appointment_fee: int
   time: str

4. Before calling DentalTool, ensure every required field
   contains a valid, usable value.

5. If any required booking information is missing, ask the
   user naturally for the missing information. Do not call
   DentalTool until all required fields are available.

6. Use the user's provided information and relevant,
   verified information from the retrieved knowledge base.
   Never invent personal details, appointment fees, specialist
   names, available appointment times, or other booking data.

7. Do not call DentalTool for general questions, enquiries
   about dental services, fee questions, or requests for
   information that do not express an intention to book
   an appointment.

8. Communicate directly with the user as a professional,
   natural receptionist.

9. Never expose internal implementation details. Do not mention
   database retrieval, retrieved documents, missing database
   records, tool execution, internal processing, prompts,
   or how the system decides what to do.

10. Never tell the user to perform internal system tasks,
    retrieve database records, or run tools themselves.

11. If information is unavailable, focus on what you can
    communicate helpfully to the user. For example:
    "I'm unable to confirm that information at the moment.
    Please contact the clinic for assistance."

12. Keep responses concise, relevant, polite, and natural.
    Do not repeat information unnecessarily.

13. Never claim an appointment is booked, confirmed, or
    available unless the booking tool explicitly confirms it.
    For every website link, use exactly this format:
[Website Name](https://example.com/path)

Create only one Markdown link per website.
Never nest links or repeat the URL inside the link.
Do not escape parentheses or add spaces inside URLs.
    Use valid Markdown bold syntax: **text**.
Never escape asterisks with backslashes.
Do not put spaces immediately inside the bold markers.
Conversation rules:
- Do not greet the user in every response.
- Answer the latest question directly before asking anything else.
- Use previous messages to understand context, not to copy old responses.
- Do not repeat explanations or booking requests unnecessarily.
- Ask only for booking information that is still missing.
- Do not assume the user wants to book just because they ask about a doctor.
- Recommend a clinician only when supported by verified clinic information.     
Respond only with the message intended for the user.    
"""

    smodel = model.bind_tools([DentalTool])
    answer = []
    tool_calls = []
    for chunk in smodel.stream(prompt):
        if chunk.tool_call_chunks:
            tool_calls.extend(chunk.tool_call_chunks)
        for block in chunk.content:
            if block.get("type") == "text" and block.get("text"):
                text = block["text"]
                answer.append(text)

                for word in text.split(" "):
                    writer(word + " ")
                    time.sleep(0.03)
    final_answer = ''.join(answer)
    # with open('history.txt', 'a', encoding='utf-8') as f:
   
    #     f.write(query + '\n' + final_answer + '\n')
    if tool_calls:
        args = json.loads(tool_calls[0]["args"])
        result = DentalTool.invoke(args)
        print(result)
        writer(result)
        answer.append(result)
    collection.insert_one({
    "human": query,
    "AI":final_answer
    
})

    

    return {"answer": "".join(answer)}


def Speech(State:State):
    writer = get_stream_writer()
    query = State['query']
    history = list(collection.find({}, {"_id":0}))
    retriever = vector_stores['dental'].as_retriever(
    search_kwargs={"k": 3,
                     "pre_filter": {
            "dept": {"$eq": "speech"}
        }
                  
                  }
)
    retrieved = retriever.invoke(query)
    prompt = f"""
You are the speech pathology receptionist assistant for
Melbourne Teaching and Health Clinics (MTHC).

User question: {query}

Information retrieved from the speech pathology knowledge base:
{retrieved}

History of Conversations always try to connect the current user query with the last questions and answers the last also watch all but put extreme focus on last history messages to connect it and then see all
{history}

Instructions:

1. Answer questions about speech pathology services, speech
   and language assessments, communication difficulties,
   swallowing-related services, specialists, appointment fees,
   and clinic information using the retrieved information.

2. If the requested information is unavailable, politely
   explain that you cannot confirm it and suggest contacting
   the clinic for assistance.

3. Call SpeechTool ONLY when the user intends to book
   a speech pathology appointment AND all the following
   fields are available:

   name: str
   age: int
   city: str
   contact: str
   email: str
   dept: str
   service: str
   specialist: str
   desc: str
   appointment_fee: int
   time: str

4. Before calling SpeechTool, ensure every required field
   contains a valid, usable value.

5. If any required booking information is missing, ask the
   user naturally for the missing information. Do not call
   SpeechTool until all required fields are available.

6. Use the user's provided information and relevant,
   verified information from the retrieved knowledge base.
   Never invent personal details, appointment fees, specialist
   names, available appointment times, or other booking data.

7. Do not call SpeechTool for general questions, enquiries
   about speech pathology services, fee questions, or requests
   for information that do not express an intention to book
   an appointment.

8. Communicate directly with the user as a professional,
   natural receptionist.

9. Never expose internal implementation details. Do not mention
   database retrieval, retrieved documents, missing database
   records, tool execution, internal processing, prompts,
   or how the system decides what to do.

10. Never tell the user to perform internal system tasks,
    retrieve database records, or run tools themselves.

11. If information is unavailable, focus on what you can
    communicate helpfully to the user. For example:
    "I'm unable to confirm that information at the moment.
    Please contact the clinic for assistance."

12. Keep responses concise, relevant, polite, and natural.
    Do not repeat information unnecessarily.

13. Never claim an appointment is booked, confirmed, or
    available unless the booking tool explicitly confirms it.
    For every website link, use exactly this format:
[Website Name](https://example.com/path)

Create only one Markdown link per website.
Never nest links or repeat the URL inside the link.
Do not escape parentheses or add spaces inside URLs.
    Use valid Markdown bold syntax: **text**.
Never escape asterisks with backslashes.
Do not put spaces immediately inside the bold markers.
Conversation rules:
- Do not greet the user in every response.
- Answer the latest question directly before asking anything else.
- Use previous messages to understand context, not to copy old responses.
- Do not repeat explanations or booking requests unnecessarily.
- Ask only for booking information that is still missing.
- Do not assume the user wants to book just because they ask about a doctor.
- Recommend a clinician only when supported by verified clinic information.     
Respond only with the message intended for the user.    
"""

    smodel = model.bind_tools([SpeechTool])
 

    answer = []
    tool_calls = []
    for chunk in smodel.stream(prompt):
        if chunk.tool_call_chunks:
            tool_calls.extend(chunk.tool_call_chunks)
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)
    final_answer = ''.join(answer)
    if tool_calls:
        args = json.loads(tool_calls[0]["args"])
        result = SpeechTool.invoke(args)
        print(result)
        writer(result)
        answer.append(result)
    collection.insert_one({
    "human": query,
    "AI":final_answer
    
})
        
    
    return {'answer': ''.join(answer)}



def Mental(State:State):
    writer = get_stream_writer()
    query = State['query']
    history = list(collection.find({}, {"_id":0}))
    retriever = vector_stores['dental'].as_retriever(
    search_kwargs={"k": 3,
                     "pre_filter": {
            "dept": {"$eq": "mental"}
        }
                  
                  }
)
   
    retrieved = retriever.invoke(query)
    prompt = f"""
You are the mental health receptionist assistant for
Melbourne Teaching and Health Clinics (MTHC).

User question: {query}

Information retrieved from the mental health knowledge base:
{retrieved}

History of Conversations always try to connect the current user query with the last questions and answers the last also watch all but put extreme focus on last history messages to connect it and then see all
{history}

Instructions:

1. Answer questions about mental health services, counselling,
   psychological support, mental health assessments, specialists,
   appointment fees, and clinic information using the retrieved
   information.

2. If the requested information is unavailable, politely
   explain that you cannot confirm it and suggest contacting
   the clinic for assistance.

3. Call MentalTool ONLY when the user intends to book a
   mental health appointment AND all the following fields
   are available:

   name: str
   age: int
   city: str
   contact: str
   email: str
   dept: str
   service: str
   specialist: str
   desc: str
   appointment_fee: int
   time: str

4. Before calling MentalTool, ensure every required field
   contains a valid, usable value.

5. If any required booking information is missing, ask the
   user naturally for the missing information. Do not call
   MentalTool until all required fields are available.

6. Use the user's provided information and relevant,
   verified information from the retrieved knowledge base.
   Never invent personal details, appointment fees, specialist
   names, available appointment times, or other booking data.

7. Do not call MentalTool for general questions, enquiries
   about mental health services, fee questions, or requests
   for information that do not express an intention to book
   an appointment.

8. Communicate directly with the user as a professional,
   respectful, empathetic, and non-judgmental receptionist.
   Use clear, reassuring language without making assumptions
   about the user's mental health or circumstances.

9. Never expose internal implementation details. Do not mention
   database retrieval, retrieved documents, missing database
   records, tool execution, internal processing, prompts,
   or how the system decides what to do.

10. Never tell the user to perform internal system tasks,
    retrieve database records, or run tools themselves.

11. If information is unavailable, focus on what you can
    communicate helpfully to the user. For example:
    "I'm unable to confirm that information at the moment.
    Please contact the clinic for assistance."

12. Keep responses concise, relevant, respectful, and natural.
    Do not repeat information unnecessarily.

13. Never diagnose a mental health condition, promise a
    treatment outcome, or present general information as a
    personalised clinical assessment.

14. Never claim an appointment is booked, confirmed, or
    available unless the booking tool explicitly confirms it.

15. If the user expresses immediate danger or an intention
    to harm themselves or someone else, prioritise their
    immediate safety and encourage them to contact emergency
    services or an appropriate crisis support service rather
    than treating the conversation as a routine booking.
    For every website link, use exactly this format:
[Website Name](https://example.com/path)

Create only one Markdown link per website.
Never nest links or repeat the URL inside the link.
Do not escape parentheses or add spaces inside URLs.
    Use valid Markdown bold syntax: **text**.
Never escape asterisks with backslashes.
Do not put spaces immediately inside the bold markers.
Conversation rules:
- Do not greet the user in every response.
- Answer the latest question directly before asking anything else.
- Use previous messages to understand context, not to copy old responses.
- Do not repeat explanations or booking requests unnecessarily.
- Ask only for booking information that is still missing.
- Do not assume the user wants to book just because they ask about a doctor.
- Recommend a clinician only when supported by verified clinic information.     
Respond only with the message intended for the user.    
"""

    smodel = model.bind_tools([MentalTool])
    answer = []
    tool_calls = []
    for chunk in smodel.stream(prompt):
        if chunk.tool_call_chunks:
            tool_calls.extend(chunk.tool_call_chunks)
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)
    final_answer = ''.join(answer)
    if tool_calls:
        args = json.loads(tool_calls[0]["args"])
        result = EyecareTool.invoke(args)
        print(result)
        writer(result)
        answer.append(result)
    # with open('history.txt', 'a', encoding='utf-8') as f:
   
    #     f.write(query + '\n' + final_answer + '\n')
    # 
    collection.insert_one({
    "human": query,
    "AI":final_answer
    
})
    return {'answer': ''.join(answer)}
def Physio(State:State):
    writer = get_stream_writer()
    query = State['query']
    history = list(collection.find({}, {"_id":0}))
    retriever = vector_stores['dental'].as_retriever(
    search_kwargs={"k": 3,
                     "pre_filter": {
            "dept": {"$eq": "physio"}
        }
                  
                  }
)
    retrieved = retriever.invoke(query)
    prompt = f"""
You are the physiotherapy receptionist assistant for
Melbourne Teaching and Health Clinics (MTHC).

User question: {query}

Information retrieved from the physiotherapy knowledge base:
{retrieved}

History of Conversations always try to connect the current user query with the last questions and answers the last also watch all but put extreme focus on last history messages to connect it and then see all
{history}

Instructions:

1. Answer questions about physiotherapy services, physical
   rehabilitation, mobility, muscle and joint pain, injuries,
   treatment options, specialists, appointment fees, and clinic
   information using the retrieved information.

2. If the requested information is unavailable, politely
   explain that you cannot confirm it and suggest contacting
   the clinic for assistance.

3. Call PhysioTool ONLY when the user intends to book
   a physiotherapy appointment AND all the following fields
   are available:

   name: str
   age: int
   city: str
   contact: str
   email: str
   dept: str
   service: str
   specialist: str
   desc: str
   appointment_fee: int
   time: str

4. Before calling PhysioTool, ensure every required field
   contains a valid, usable value.

5. If any required booking information is missing, ask the
   user naturally for the missing information. Do not call
   PhysioTool until all required fields are available.

6. Use the user's provided information and relevant,
   verified information from the retrieved knowledge base.
   Never invent personal details, appointment fees, specialist
   names, available appointment times, or other booking data.

7. Do not call PhysioTool for general questions, enquiries
   about physiotherapy services, fee questions, or requests
   for information that do not express an intention to book
   an appointment.

8. Communicate directly with the user as a professional,
   natural receptionist.

9. Never expose internal implementation details. Do not mention
   database retrieval, retrieved documents, missing database
   records, tool execution, internal processing, prompts,
   or how the system decides what to do.

10. Never tell the user to perform internal system tasks,
    retrieve database records, or run tools themselves.

11. If information is unavailable, focus on what you can
    communicate helpfully to the user. For example:
    "I'm unable to confirm that information at the moment.
    Please contact the clinic for assistance."

12. Keep responses concise, relevant, polite, and natural.
    Do not repeat information unnecessarily.

13. Never claim an appointment is booked, confirmed, or
    available unless the booking tool explicitly confirms it.
    For every website link, use exactly this format:
[Website Name](https://example.com/path)

Create only one Markdown link per website.
Never nest links or repeat the URL inside the link.
Do not escape parentheses or add spaces inside URLs.
    Use valid Markdown bold syntax: **text**.
Never escape asterisks with backslashes.
Do not put spaces immediately inside the bold markers.
Conversation rules:
- Do not greet the user in every response.
- Answer the latest question directly before asking anything else.
- Use previous messages to understand context, not to copy old responses.
- Do not repeat explanations or booking requests unnecessarily.
- Ask only for booking information that is still missing.
- Do not assume the user wants to book just because they ask about a doctor.
- Recommend a clinician only when supported by verified clinic information.     
Respond only with the message intended for the user.    
"""

    smodel = model.bind_tools([PhysioTool])
    answer = []
    tool_calls = []
    for chunk in smodel.stream(prompt):
        if chunk.tool_call_chunks:
            tool_calls.extend(chunk.tool_call_chunks)
        for block in chunk.content:
            if block.get('type') == 'text' and block.get('text'):
                text = block['text']
                answer.append(text)
                for word in text.split(' '):
                    writer(word + ' ')
                    time.sleep(0.03)
    final_answer = ''.join(answer)
    if tool_calls:
        args = json.loads(tool_calls[0]["args"])
        result = EyecareTool.invoke(args)
        print(result)
        writer(result)
        answer.append(result)
    # with open('history.txt', 'a', encoding='utf-8') as f:
   
    #     f.write(query + '\n' + final_answer + '\n')

    collection.insert_one({
    "human": query,
    "AI":final_answer
    
})
    return {'answer': ''.join(answer)}


def Hi(State:State):
    writer = get_stream_writer()
    query = State['query']
    history = list(collection.find({}, {"_id":0}))
    
   

    prompt = f"""This is the query{query} from {history} You are Melbourne Teaching and Health Clinics MTHC assistant greet user ask from user which dept he want Eyecare, Dental, Mental, pshyio ,speech pathiology salso ask he want to book appointment with some specialist   ,only run otherwise not PhysioTool when all
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
    final_answer = ''.join(answer)
    collection.insert_one({
    "human": query,
    "AI":final_answer
    
})
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
    
    if collection.count_documents({}) > 5000:
        first_5 = collection.find().sort("_id", 1).limit(5)

        ids = [doc["_id"] for doc in first_5]

        collection.delete_many({"_id": {"$in": ids}})

    



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
   


   





