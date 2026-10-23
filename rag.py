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

  """
  Staff / Team
Dr. Fiona Bailey
Dr. Fiona Bailey
Clinical Psychologist – Director, UoMPC
Fiona is a clinical psychologist based in Melbourne and Director of the University of Melbourne Psychology Clinic. Fiona also owns and works within a private practice in Essendon, Victoria. With an interest in adult mental health, perinatal mental health, psychotherapy and treatment of mental health conditions, Fiona maintains a busy private practice at Junction Health Psychology and works as the Director of the University of Melbourne Psychology Clinic. She is a Clinical Supervisor and provides supervision to provisionally registered psychologists and those seeking Clinical endorsement. She is a Founding member of the Australian Clinical Psychology Association (ACPA).

Portrait of Maria Tandoc, Registered Psychologist specialising in educational and developmental psychology at MTHC Psychology Clinic.
Maria Tandoc
Psychologist
Maria is a registered Psychologist with a Master in Educational and Developmental Psychology from the Australian Catholic University and Bachelor of Science (First Class Honours) with Monash University. Maria has worked in various support roles in different educational and private settings. Maria has a particular interest in accessible and equitable education, as well as providing counselling and strategies to assist individuals in navigating challenges and meeting their goals. With a neuroaffirming approach, Maria prioritises a collaborative, client-centred, collaborative and strength-based focus within the therapy space.

Maria works across the lifespan, counselling children, adolescents and adults. She is trained in the provision of psychoeducational assessments, treatment planning and interventions. She can assist in the exploration of cognitive, behavioural, attentional and adaptive difficulties in children, adolescents and adults.

Della Tanri
Della Tanri
Psychologist, Educational and Developmental Psychology Registrar
Della is an early career psychologist with an interest in neurodivergence and psychoeducational assessments. Della completed her Masters in Educational and Developmental Psychology from Monash University. Della’s experiences ranges from working in primary and highschool settings to conducting lifespan psychoeducational assessments and intervention in community health settings.

Della has training conducting psychoeducational assessments across the lifespan, across a diverse range of concerns. Della also has experience with one-on-one counselling and intervention with both children and adults for a range of presentations including, anxiety, depression, social skills difficulties, emotion regulation, and grief. Fluent in English and Indonesian. Della is deeply passionate about working with culturally and linguistically diverse communities.

Professional portrait of Lydia Soh, Educational and Developmental Psychologist and Board Approved Supervisor specialising in assessments for Specific Learning Disorders, ADHD and Autism Spectrum Disorder at MTHC Psychology Clinic.
Dr Lydia Soh
Educational & Developmental psychologist
Lydia is an Educational & Developmental psychologist and Board Approved Supervisor with a passion for supporting children, young people, and their families to understand their strengths, navigate challenges, and thrive. She has a particular interest in the assessment of Specific Learning Disorders, Attention-Deficit/Hyperactivity Disorder (ADHD), and Autism Spectrum Disorder (ASD). Through the assessment process, Lydia aims to help individuals and families gain a clear understanding of the person’s unique profile and support needs. In her therapeutic work, Lydia draws on a range of evidence-based approaches, including cognitive behaviour therapy, acceptance and commitment therapy, and mindfulness-based strategies. She values working collaboratively with parents, caregivers, and schools to achieve meaningful outcomes for every child.
  """


]
metadatas = [{"dept": "mental"} for _ in data]


db.add_texts(data,
metadatas=metadatas)
print("added Successfully")