from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from dotenv import load_dotenv
import os
load_dotenv()

API = os.getenv("API")
embedding = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")
client = MongoClient(API)
database = client['MTHC']
collection = database['dental']
db = MongoDBAtlasVectorSearch(
    embedding = embedding,
    collection = collection,
    index_name = "vector_index"
)



data = [


]



db.add_texts(data)
print("added Successfully")